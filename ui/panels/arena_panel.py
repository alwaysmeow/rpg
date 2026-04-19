import pyglet

from ui.panel import Panel
from ui.hud.clock import Clock, PANEL_W, PANEL_H
from ui.hud.unit_card import UnitCard, DEFAULT_CARD_W, DEFAULT_CARD_H

CARD_GAP  = 10
TEAM_PAD  = 16
VS_GAP    = 60
VS_SIZE   = 24


class ArenaPanel(Panel):
    def __init__(self, batch, group_bg, group_bar, group_text):
        self._batch  = batch
        self._g_bg   = group_bg
        self._g_bar  = group_bar
        self._g_text = group_text

        self._x = self._y = self._w = self._h = 0

        self._clock: Clock | None = None
        self._vs_label: pyglet.text.Label | None = None

        # team_index -> {unit_id: UnitCard}
        self._cards: dict[int, dict[int, UnitCard]] = {0: {}, 1: {}}

    def unit_at(self, px: int, py: int) -> int | None:
        for team in (0, 1):
            for unit_id, card in self._cards[team].items():
                if card.contains(px, py):
                    return unit_id
        return None

    def resize(self, x: int, y: int, w: int, h: int) -> None:
        self._x, self._y, self._w, self._h = x, y, w, h
        self._rebuild_static()
        self._reposition_all_cards()

    def update(self, snapshot, dt: float) -> None:
        if snapshot is None:
            return

        if self._clock:
            self._clock.update(snapshot.time)

        entities = snapshot.entities

        units:     dict[int, dict] = {}
        abilities: dict[int, dict] = {}

        for eid_raw, data in entities.items():
            eid  = int(eid_raw)
            tags = data.get("Tags", [])
            if "Unit" in tags:
                units[eid] = data
            if "Ability" in tags:
                abilities[eid] = data

        ability_by_owner: dict[int, dict] = {}
        for ab in abilities.values():
            owner_id = ab.get("Owner", {}).get("unit_id")
            if owner_id is not None:
                ability_by_owner[int(owner_id)] = ab

        # Группируем по командам
        by_team: dict[int, dict[int, dict]] = {0: {}, 1: {}}
        for eid, data in units.items():
            team = data.get("CombatParticipation", {}).get("team_index")
            if team in by_team:
                by_team[team][eid] = data

        needs_reposition = False
        for team in (0, 1):
            current = set(by_team[team].keys())
            existing = set(self._cards[team].keys())

            for eid in existing - current:
                self._cards[team].pop(eid).delete()
                needs_reposition = True

            for eid in sorted(current - existing):
                self._cards[team][eid] = self._make_card(team)
                needs_reposition = True

        if needs_reposition:
            self._reposition_all_cards()

        for team in (0, 1):
            for eid, card in self._cards[team].items():
                card.update(by_team[team][eid], ability_by_owner.get(eid), dt)

    def delete(self) -> None:
        if self._clock:
            self._clock.delete()
        if self._vs_label:
            self._vs_label.delete()
        for team_cards in self._cards.values():
            for card in team_cards.values():
                card.delete()
        self._cards = {0: {}, 1: {}}

    def _card_w(self) -> int:
        """Ширина карточки = половина панели минус отступы и половина VS-зазора."""
        return max(160, (self._w - VS_GAP) // 2 - TEAM_PAD * 2)

    def _card_h(self) -> int:
        """Высота карточки — не больше трети высоты панели."""
        return min(DEFAULT_CARD_H, max(80, self._h // 3))

    def _rebuild_static(self) -> None:
        cx = self._x + self._w // 2
        top = self._y + self._h

        if self._clock:
            self._clock.delete()
        clock_x = cx - PANEL_W // 2
        clock_y = top - PANEL_H - 8
        self._clock = Clock(clock_x, clock_y, self._batch, self._g_bg, self._g_text)

        vs_y = self._y + self._h // 2
        if self._vs_label is None:
            self._vs_label = pyglet.text.Label(
                "VS", font_name="Courier New", font_size=VS_SIZE,
                x=cx, y=vs_y,
                anchor_x="center", anchor_y="center",
                color=(180, 80, 80, 255),
                batch=self._batch, group=self._g_text,
            )
        else:
            self._vs_label.x = cx
            self._vs_label.y = vs_y

    def _make_card(self, team: int) -> UnitCard:
        return UnitCard(
            self._x, self._y,
            team,
            self._batch,
            self._g_bg, self._g_bar, self._g_text,
            card_w=self._card_w(),
            card_h=self._card_h(),
        )

    def _reposition_all_cards(self) -> None:
        cw  = self._card_w()
        ch  = self._card_h()
        cx  = self._x + self._w // 2
        top = self._y + self._h - PANEL_H - 16

        col0_x = self._x + TEAM_PAD
        col1_x = cx + VS_GAP // 2

        for team, col_x in ((0, col0_x), (1, col1_x)):
            for i, card in enumerate(self._cards[team].values()):
                cy = top - (i + 1) * ch - i * CARD_GAP
                card.move(col_x, cy)
                card.resize(cw, ch)
