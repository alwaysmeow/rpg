import pyglet
from pyglet import shapes

from ui.panel import Panel
from ui.hud.clock import Clock, PANEL_W, PANEL_H
from ui.hud.resource_bar import ResourceBar
from ui.color import Color

CD_BAR_W = 140
CD_BAR_H = 6
CD_GAP   = 18


class CombatPanel(Panel):
    """
    Центральная панель: таймер боя, надпись VS, кулдауны способностей.
    """

    def __init__(self, batch, group_bg, group_text):
        self._batch = batch
        self._g_bg   = group_bg
        self._g_text = group_text
        self._g_bar  = pyglet.graphics.Group(order=1)

        self._x = self._y = self._w = self._h = 0

        self._clock: Clock | None = None
        self._vs_label: pyglet.text.Label | None = None
        self._cd_bars: dict[int, ResourceBar] = {}

    # ------------------------------------------------------------------

    def resize(self, x: int, y: int, w: int, h: int) -> None:
        self._x, self._y, self._w, self._h = x, y, w, h
        self._rebuild_static()

    def update(self, snapshot, dt: float) -> None:
        if snapshot is None:
            return

        if self._clock:
            self._clock.update(snapshot.time)

        # Собираем ability-entities
        abilities: dict[int, dict] = {
            int(eid): data
            for eid, data in snapshot.entities.items()
            if "Ability" in data.get("Tags", [])
        }

        current_ids = set(abilities.keys())
        bar_ids     = set(self._cd_bars.keys())

        for eid in bar_ids - current_ids:
            self._cd_bars.pop(eid).delete()

        if current_ids - bar_ids:
            for eid in sorted(current_ids - bar_ids):
                self._cd_bars[eid] = self._make_cd_bar(eid)
            self._reposition_cd_bars()

        for eid, bar in self._cd_bars.items():
            cd = abilities[eid].get("Cooldown", {})
            ratio = cd.get("_value_ratio", 0.0)
            bar.set_target(ratio, f"CD {ratio * 100:.0f}%")
            bar.tick(dt)

    def delete(self) -> None:
        if self._clock:
            self._clock.delete()
        if self._vs_label:
            self._vs_label.delete()
        for bar in self._cd_bars.values():
            bar.delete()
        self._cd_bars.clear()

    # ------------------------------------------------------------------

    def _rebuild_static(self) -> None:
        cx = self._x + self._w // 2
        cy = self._y + self._h // 2

        if self._clock:
            self._clock.delete()
        clock_x = cx - PANEL_W // 2
        clock_y = self._y + self._h - PANEL_H - 8
        self._clock = Clock(clock_x, clock_y, self._batch, self._g_bg, self._g_text)

        if self._vs_label is None:
            self._vs_label = pyglet.text.Label(
                "VS", font_name="Courier New", font_size=22,
                x=cx, y=cy,
                anchor_x="center", anchor_y="center",
                color=(180, 80, 80, 255),
                batch=self._batch, group=self._g_text,
            )
        else:
            self._vs_label.x = cx
            self._vs_label.y = cy

        self._reposition_cd_bars()

    def _make_cd_bar(self, ability_id: int) -> ResourceBar:
        cx = self._x + self._w // 2
        return ResourceBar(
            cx - CD_BAR_W // 2, self._y,
            CD_BAR_W, CD_BAR_H,
            fg_color=Color.UNIT_CD_FG.rgba,
            bg_color=Color.UNIT_CD_BG.rgba,
            ghost_color=Color.COMBAT_DONE.rgba,
            label_text="CD",
            batch=self._batch,
            group_bg=self._g_bg,
            group_bar=self._g_bar,
            group_text=self._g_text,
        )

    def _reposition_cd_bars(self) -> None:
        cx = self._x + self._w // 2
        for i, bar in enumerate(self._cd_bars.values()):
            by = self._y + 16 + i * CD_GAP
            bar.move(cx - CD_BAR_W // 2, by)
