import pyglet
from pyglet import shapes

from ui.color import Color
from ui.hud.resource_bar import ResourceBar

DEFAULT_CARD_W = 200
DEFAULT_CARD_H = 300
PADDING        = 12
FONT_SIZE      = 20

HP_H = 12
MP_H = 12
ST_H = 12

class UnitCard:
    def __init__(
        self,
        x: int, y: int,
        team_index: int,
        batch: pyglet.graphics.Batch,
        group_bg, group_bar, group_text,
        card_w: int = DEFAULT_CARD_W,
        card_h: int = DEFAULT_CARD_H,
    ):
        self.x = x
        self.y = y
        self.team_index = team_index
        self._batch  = batch
        self._g_bg   = group_bg
        self._g_bar  = group_bar
        self._g_text = group_text
        self._w = card_w
        self._h = card_h

        team_color = Color.UNIT_TEAM_0 if team_index == 0 else Color.UNIT_TEAM_1

        self._bg = shapes.RoundedRectangle(
            x, y, card_w, card_h, radius=8,
            color=Color.UNIT_BG.rgb, batch=batch, group=group_bg,
        )
        self._bg.opacity = Color.UNIT_BG.alpha

        self._border = shapes.RoundedRectangle(
            x, y, card_w, card_h, radius=8,
            color=team_color.rgb, batch=batch, group=group_bg,
        )
        self._border.opacity = 55

        self._team_bar = shapes.Rectangle(
            x + 4, y + card_h - 5, card_w - 8, 4,
            color=team_color.rgb, batch=batch, group=group_bar,
        )
        self._team_bar.opacity = team_color.alpha

        self._name_label = pyglet.text.Label(
            "", font_name="Courier New", font_size=FONT_SIZE,
            x=x + PADDING, y=y + card_h - PADDING - FONT_SIZE,
            color=Color.UNIT_TEXT.rgba,
            batch=batch, group=group_text,
        )

        self._hp_bar: ResourceBar | None = None
        self._mp_bar: ResourceBar | None = None
        self._st_bar: ResourceBar | None = None
        self._rebuild_bars()

        self._dead_overlay = shapes.Rectangle(
            x, y, card_w, card_h,
            color=Color.UNIT_DEAD.rgb, batch=batch, group=group_bar,
        )
        self._dead_overlay.opacity = 0

        self._dead_label = pyglet.text.Label(
            "DEAD", font_name="Courier New", font_size=FONT_SIZE,
            x=x + card_w // 2, y=y + card_h // 2,
            anchor_x="center", anchor_y="center",
            color=(220, 60, 60, 0),
            batch=batch, group=group_text,
        )

    def update(self, unit_data: dict, ability_data: dict | None, dt: float) -> None:
        self._name_label.text = unit_data.get("Name", {}).get("name", "???")

        health   = unit_data.get("Health", {})
        hp_ratio = health.get("_value_ratio", 1.0)
        hp_max   = health.get("effective_max_value", 100)
        self._hp_bar.set_target(hp_ratio, f"HP {round(hp_ratio * hp_max)}/{hp_max}")

        mana = unit_data.get("Mana", {})
        if mana:
            mp_ratio = mana.get("_value_ratio", 1.0)
            mp_max   = mana.get("effective_max_value", 100)
            self._mp_bar.set_target(mp_ratio, f"MP {round(mp_ratio * mp_max)}/{mp_max}")
        else:
            self._mp_bar.set_target(0.0, "MP —")

        stamina = unit_data.get("Stamina", {})
        if stamina:
            st_ratio = stamina.get("_value_ratio", 1.0)
            st_max   = stamina.get("effective_max_value", 100)
            self._st_bar.set_target(st_ratio, f"ST {round(st_ratio * st_max)}/{st_max}")
        else:
            self._st_bar.set_target(0.0, "ST —")

        self._hp_bar.tick(dt)
        self._mp_bar.tick(dt)
        self._st_bar.tick(dt)

        tags  = unit_data.get("Tags", [])
        alpha = 160 if "Dead" in tags else 0
        self._dead_overlay.opacity = alpha
        self._dead_label.color = (220, 60, 60, alpha)

    def move(self, x: int, y: int) -> None:
        dx, dy = x - self.x, y - self.y
        if dx == 0 and dy == 0:
            return
        self.x, self.y = x, y
        for obj in (self._bg, self._border, self._team_bar, self._dead_overlay):
            obj.x += dx
            obj.y += dy
        self._name_label.x += dx
        self._name_label.y += dy
        self._dead_label.x += dx
        self._dead_label.y += dy
        for bar in (self._hp_bar, self._mp_bar, self._st_bar):
            bar.move(bar._x + dx, bar._y + dy)

    def resize(self, w: int, h: int) -> None:
        if w == self._w and h == self._h:
            return
        self._w, self._h = w, h

        for obj in (self._bg, self._border, self._team_bar,
                    self._dead_overlay, self._dead_label):
            obj.delete()
        for bar in (self._hp_bar, self._mp_bar, self._st_bar):
            if bar:
                bar.delete()

        team_color = Color.UNIT_TEAM_0 if self.team_index == 0 else Color.UNIT_TEAM_1
        x, y = self.x, self.y

        self._bg = shapes.RoundedRectangle(
            x, y, w, h, radius=8,
            color=Color.UNIT_BG.rgb, batch=self._batch, group=self._g_bg,
        )
        self._bg.opacity = Color.UNIT_BG.alpha

        self._border = shapes.RoundedRectangle(
            x, y, w, h, radius=8,
            color=team_color.rgb, batch=self._batch, group=self._g_bg,
        )
        self._border.opacity = 55

        self._team_bar = shapes.Rectangle(
            x + 4, y + h - 5, w - 8, 4,
            color=team_color.rgb, batch=self._batch, group=self._g_bar,
        )
        self._team_bar.opacity = team_color.alpha

        self._dead_overlay = shapes.Rectangle(
            x, y, w, h,
            color=Color.UNIT_DEAD.rgb, batch=self._batch, group=self._g_bar,
        )
        self._dead_overlay.opacity = 0

        self._dead_label = pyglet.text.Label(
            "DEAD", font_name="Courier New", font_size=FONT_SIZE,
            x=x + w // 2, y=y + h // 2,
            anchor_x="center", anchor_y="center",
            color=(220, 60, 60, 0),
            batch=self._batch, group=self._g_text,
        )

        self._name_label.x = x + PADDING
        self._name_label.y = y + h - PADDING - FONT_SIZE

        self._rebuild_bars()

    def _rebuild_bars(self) -> None:
        for bar in (self._hp_bar, self._mp_bar, self._st_bar):
            if bar:
                bar.delete()

        x, y    = self.x, self.y
        bar_w   = self._w - PADDING * 2
        ghost   = Color.UNIT_HP_GHOST.rgba

        bar_area_h = self._h - PADDING * 2 - FONT_SIZE - 8
        slot_h     = max(1, bar_area_h // 3)

        self._hp_bar = ResourceBar(
            x + PADDING, y + PADDING + slot_h * 2, bar_w, HP_H,
            fg_color=Color.UNIT_HP_FG.rgba,
            bg_color=Color.UNIT_HP_BG.rgba,
            ghost_color=ghost, label_text="HP",
            batch=self._batch,
            group_bg=self._g_bg, group_bar=self._g_bar, group_text=self._g_text,
        )
        self._mp_bar = ResourceBar(
            x + PADDING, y + PADDING + slot_h, bar_w, MP_H,
            fg_color=Color.UNIT_CD_FG.rgba,
            bg_color=Color.UNIT_CD_BG.rgba,
            ghost_color=ghost, label_text="MP",
            batch=self._batch,
            group_bg=self._g_bg, group_bar=self._g_bar, group_text=self._g_text,
        )
        self._st_bar = ResourceBar(
            x + PADDING, y + PADDING, bar_w, ST_H,
            fg_color=Color.COMBAT_ACTIVE.rgba,
            bg_color=Color.UNIT_CD_BG.rgba,
            ghost_color=ghost, label_text="ST",
            batch=self._batch,
            group_bg=self._g_bg, group_bar=self._g_bar, group_text=self._g_text,
        )

    def delete(self) -> None:
        for obj in (self._bg, self._border, self._team_bar,
                    self._dead_overlay, self._dead_label, self._name_label):
            obj.delete()
        for bar in (self._hp_bar, self._mp_bar, self._st_bar):
            if bar:
                bar.delete()