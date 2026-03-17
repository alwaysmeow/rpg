import threading
import pyglet
from pyglet import shapes

from ui.color import Color
from ui.hud.unit_card import UnitCard, CARD_W, CARD_H
from ui.hud.clock import Clock, PANEL_W, PANEL_H

MARGIN = 20
VS_LABEL_COLOR = (180, 80, 80, 255)


class HUDWindow(pyglet.window.Window):
    def __init__(self, bridge, *args, **kwargs):
        kwargs.setdefault("caption", "Combat HUD")
        kwargs.setdefault("resizable", True)
        super().__init__(*args, **kwargs)

        self._bridge = bridge
        self._lock = threading.Lock()

        self._fps = 0.0
        self._fps_acc = 0.0
        self._fps_frames = 0

        pyglet.gl.glClearColor(
            Color.BACKGROUND.red / 255, Color.BACKGROUND.green / 255,
            Color.BACKGROUND.blue / 255, 1.0
        )

        self._batch = pyglet.graphics.Batch()

        # Группы для упорядоченной отрисовки
        self._g_bg   = pyglet.graphics.Group(order=0)
        self._g_bar  = pyglet.graphics.Group(order=1)
        self._g_text = pyglet.graphics.Group(order=2)

        # Объекты HUD — создаются один раз, обновляются данными из снапшота
        self._unit_cards: dict[int, UnitCard] = {}
        self._combat_panel: Clock | None = None
        self._vs_label: pyglet.text.Label | None = None
        self._fps_label = pyglet.text.Label(
            "", font_name="Courier New", font_size=8,
            x=6, y=6, color=(80, 80, 100, 200),
            batch=self._batch, group=self._g_text
        )

        self._last_snapshot = None

        pyglet.clock.schedule_interval(self._tick, 1 / 30)

    # ------------------------------------------------------------------
    # Pyglet callbacks
    # ------------------------------------------------------------------

    def on_draw(self):
        self.clear()
        self._batch.draw()

    def on_resize(self, w, h):
        super().on_resize(w, h)
        self._rebuild_layout()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()

    # ------------------------------------------------------------------
    # Tick: читаем снапшот и обновляем HUD
    # ------------------------------------------------------------------

    def _tick(self, dt):
        snapshot = self._bridge.latest_snapshot()
        if snapshot is None or snapshot is self._last_snapshot:
            self._fps_acc += dt
            self._fps_frames += 1
            if self._fps_acc >= 0.5:
                self._fps = self._fps_frames / self._fps_acc
                self._fps_acc = 0.0
                self._fps_frames = 0
            self._fps_label.text = f"FPS {self._fps:.0f}"
            return
        self._last_snapshot = snapshot
        self._apply_snapshot(snapshot)

    def _apply_snapshot(self, snapshot):
        entities = snapshot.entities
        sim_time = snapshot.time

        # Разбираем сущности из снапшота
        units: dict[int, dict] = {}
        abilities: dict[int, dict] = {}
        combats: dict[int, dict] = {}

        for eid_raw, data in entities.items():
            eid = int(eid_raw)
            tags = data.get("Tags", [])
            if "Unit" in tags:
                units[eid] = data
            if "Ability" in tags:
                abilities[eid] = data
            if "Combat" in tags:
                combats[eid] = data

        # Строим map: unit_id -> ability_data
        ability_by_owner: dict[int, dict] = {}
        for ab in abilities.values():
            owner_id = ab.get("Owner", {}).get("unit_id")
            if owner_id is not None:
                ability_by_owner[int(owner_id)] = ab

        # Строим карточки (только при первом появлении или изменении набора)
        current_ids = set(units.keys())
        card_ids = set(self._unit_cards.keys())

        if current_ids != card_ids:
            for eid in card_ids - current_ids:
                self._unit_cards[eid].delete()
                del self._unit_cards[eid]
            for eid in current_ids - card_ids:
                team = units[eid].get("CombatParticipation", {}).get("team_index", 0)
                card = self._make_unit_card(eid, team, len(self._unit_cards))
                self._unit_cards[eid] = card
            self._rebuild_layout()

        for eid, card in self._unit_cards.items():
            card.update(units[eid], ability_by_owner.get(eid))

        if self._combat_panel:
            self._combat_panel.update(sim_time)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _make_unit_card(self, unit_id: int, team_index: int, slot: int) -> UnitCard:
        x, y = self._card_position(slot, team_index)
        return UnitCard(x, y, team_index, self._batch,
                        self._g_bg, self._g_bar, self._g_text)

    def _card_position(self, slot: int, team_index: int) -> tuple[int, int]:
        w, h = self.width, self.height
        center_y = h // 2 - CARD_H // 2

        if team_index == 0:
            x = MARGIN
        else:
            x = w - MARGIN - CARD_W

        y = center_y - slot * (CARD_H + MARGIN // 2)
        return x, y

    def _rebuild_layout(self):
        w, h = self.width, self.height

        # Переставляем карточки
        team_slots: dict[int, int] = {0: 0, 1: 0}
        for eid, card in self._unit_cards.items():
            team = card.team_index
            slot = team_slots[team]
            team_slots[team] += 1
            nx, ny = self._card_position(slot, team)
            # Перемещаем все объекты карточки — проще пересоздать позиции
            dx = nx - card.x
            dy = ny - card.y
            if dx == 0 and dy == 0:
                continue
            card.x = nx
            card.y = ny
            self._shift_card(card, dx, dy)

        # Панель боя по центру сверху
        if self._combat_panel is None:
            px = w // 2 - PANEL_W // 2
            py = h - MARGIN - PANEL_H
            self._combat_panel = Clock(
                px, py, self._batch, self._g_bg, self._g_text
            )
        else:
            pass  # Пересоздаём при изменении размера — опционально

        # VS надпись
        if self._vs_label is None:
            self._vs_label = pyglet.text.Label(
                "VS", font_name="Courier New", font_size=24,
                x=w // 2, y=h // 2,
                anchor_x="center", anchor_y="center",
                color=VS_LABEL_COLOR,
                batch=self._batch, group=self._g_text
            )

    @staticmethod
    def _shift_card(card: UnitCard, dx: int, dy: int):
        """Сдвигает все shapes и labels карточки на (dx, dy)."""
        shape_attrs = [
            "_bg", "_border", "_team_bar",
            "_hp_bg", "_hp_bar",
            "_cd_bg", "_cd_bar",
            "_dead_overlay",
        ]
        label_attrs = [
            "_name_label", "_hp_label",
            "_stats_label", "_cd_label",
            "_dead_label",
        ]
        for attr in shape_attrs:
            obj = getattr(card, attr, None)
            if obj:
                obj.x += dx
                obj.y += dy
        for attr in label_attrs:
            obj = getattr(card, attr, None)
            if obj:
                obj.x += dx
                obj.y += dy

    def sink(self, text):
        pass