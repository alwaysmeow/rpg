import pyglet
from pyglet import shapes

from ui.color import Color

PANEL_W = 300
PANEL_H = 60

FONT_SIZE = 30

class Clock:
    def __init__(self, x: int, y: int, batch: pyglet.graphics.Batch,
                 bg_group, text_group):
        self._bg = shapes.RoundedRectangle(
            x, y, PANEL_W, PANEL_H, radius=6,
            color=Color.COMBAT_BG.rgb, batch=batch, group=bg_group
        )
        self._bg.opacity = Color.COMBAT_BG.alpha

        label_kwargs = dict(font_name="Courier New", batch=batch, group=text_group)

        self._time_label = pyglet.text.Label(
            "", font_size=FONT_SIZE,
            x=x + PANEL_W // 2, y=y + PANEL_H // 2,
            anchor_x="center", anchor_y="center",
            color=Color.COMBAT_LABEL,
            **label_kwargs
        )

    def update(self, sim_time: float):
        seconds = int(sim_time)
        minutes = seconds // 60
        seconds %= 60
        self._time_label.text = f"{minutes:02d}:{seconds:02d}"

    def delete(self):
        for obj in [self._bg, self._time_label]:
            obj.delete()