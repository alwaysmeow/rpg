import pyglet
from pyglet import shapes

from ui.color import Color

CARD_W = 600
CARD_H = 400
PADDING = 12
BAR_H = 10
BAR_W = CARD_W - PADDING * 2

FONT_SIZE = 30

class UnitCard:
    def __init__(self, x: int, y: int, team_index: int, batch: pyglet.graphics.Batch,
                 bg_group, bar_group, text_group):
        self.x = x
        self.y = y
        self._batch = batch
        self._bg_group = bg_group
        self._bar_group = bar_group
        self._text_group = text_group
        self.team_index = team_index

        team_color = Color.UNIT_TEAM_0 if team_index == 0 else Color.UNIT_TEAM_1

        self._bg = shapes.RoundedRectangle(
            x, y, CARD_W, CARD_H, radius=8,
            color=Color.UNIT_BG.rgb, batch=batch, group=bg_group
        )
        self._bg.opacity = Color.UNIT_BG.alpha

        self._border = shapes.RoundedRectangle(
            x, y, CARD_W, CARD_H, radius=8,
            color=team_color.rgb, batch=batch, group=bg_group
        )
        self._border.opacity = 60

        self._team_bar = shapes.Rectangle(
            x + 4, y + CARD_H - 6, CARD_W - 8, 4,
            color=team_color.rgb, batch=batch, group=bar_group
        )
        self._team_bar.opacity = team_color.alpha

        bar_y = y + PADDING + FONT_SIZE * 3
        self._hp_bg = shapes.Rectangle(
            x + PADDING, bar_y, BAR_W, BAR_H,
            color=Color.UNIT_HP_BG.rgb, batch=batch, group=bar_group
        )
        self._hp_bg.opacity = Color.UNIT_HP_BG.alpha

        self._hp_bar = shapes.Rectangle(
            x + PADDING, bar_y, BAR_W, BAR_H,
            color=Color.UNIT_HP_FG.rgb, batch=batch, group=bar_group
        )
        self._hp_bar.opacity = Color.UNIT_HP_FG.alpha

        cd_y = y + PADDING + FONT_SIZE
        self._cd_bg = shapes.Rectangle(
            x + PADDING, cd_y, BAR_W, BAR_H - 4,
            color=Color.UNIT_CD_BG.rgb, batch=batch, group=bar_group
        )
        self._cd_bg.opacity = Color.UNIT_CD_BG.alpha

        self._cd_bar = shapes.Rectangle(
            x + PADDING, cd_y, 0, BAR_H - 4,
            color=Color.UNIT_CD_FG.rgb, batch=batch, group=bar_group
        )
        self._cd_bar.opacity = Color.UNIT_CD_FG.alpha

        self._dead_overlay = shapes.Rectangle(
            x, y, CARD_W, CARD_H,
            color=Color.UNIT_DEAD.rgb, batch=batch, group=bar_group
        )
        self._dead_overlay.opacity = 0

        label_kwargs = dict(font_name="Courier New", batch=batch, group=text_group)

        self._name_label = pyglet.text.Label(
            "", font_size=FONT_SIZE,
            x=x + PADDING, y=y + CARD_H - PADDING - FONT_SIZE,
            color=Color.UNIT_TEXT,
            **label_kwargs
        )

        self._hp_label = pyglet.text.Label(
            "", font_size=FONT_SIZE,
            x=x + PADDING, y=bar_y + BAR_H + PADDING,
            color=Color.UNIT_LABEL,
            **label_kwargs
        )

        self._cd_label = pyglet.text.Label(
            "", font_size=FONT_SIZE,
            x=x + PADDING, y=cd_y + BAR_H + PADDING,
            color=Color.UNIT_LABEL,
            **label_kwargs
        )

        self._dead_label = pyglet.text.Label(
            "DEAD", font_size=FONT_SIZE,
            x=x + CARD_W // 2, y=y + CARD_H // 2,
            anchor_x="center", anchor_y="center",
            color=(220, 60, 60, 0),
            **label_kwargs
        )

    def update(self, unit_data: dict, ability_data: dict | None):
        # Name
        self._name_label.text = unit_data.get("Name", {}).get("name", "???")

        # HP
        health = unit_data.get("Health", {})
        hp_ratio = health.get("_value_ratio", 1.0)
        hp_max = health.get("effective_max_value", 100)
        hp_val = round(hp_ratio * hp_max)

        self._hp_bar.width = max(0, int(BAR_W * hp_ratio))
        self._hp_label.text = f"HP  {hp_val} / {hp_max}"

        # Cooldown
        if ability_data:
            cd = ability_data.get("Cooldown", {})
            cd_ratio = cd.get("_value_ratio", 1.0)
            self._cd_bar.width = max(0, int(BAR_W * cd_ratio))
            self._cd_label.text = f"CD  {cd_ratio * 100:.0f}%"
        else:
            self._cd_bar.width = 0
            self._cd_label.text = "CD  —"

        # Dead overlay
        tags = unit_data.get("Tags", [])
        alpha = 160 if "Dead" in tags else 0
        self._dead_overlay.opacity = alpha
        self._dead_label.color = (220, 60, 60, alpha)

    def delete(self):
        for obj in [
            self._bg, self._border, self._team_bar,
            self._hp_bg, self._hp_bar,
            self._cd_bg, self._cd_bar,
            self._dead_overlay,
            self._name_label, self._hp_label,
            self._cd_label, self._dead_label,
        ]:
            obj.delete()