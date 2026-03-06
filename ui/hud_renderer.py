import pyglet

from ui.hud_window import HUDWindow

class HUDRenderer:
    def __init__(self, bridge = None, width: int = 900, height: int = 520):
        self._width = width
        self._height = height
        self._window: HUDWindow | None = None
        self.bridge = bridge

    def run(self):
        self._window = HUDWindow(
            self.bridge,
            width=self._width,
            height=self._height,
        )
        pyglet.app.run()

    def get_sink(self):
        return lambda text: None