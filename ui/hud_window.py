import pyglet

from ui.color import Color
from ui.layout import Layout, Slot


class HUDWindow(pyglet.window.Window):
    """
    Pyglet-окно. Не знает о панелях напрямую — только держит Layout
    и пробрасывает ему resize/tick.

    Панели регистрируются снаружи через self.layout.add_panel(slot, panel).
    """

    def __init__(self, bridge, *args, **kwargs):
        kwargs.setdefault("caption", "Combat HUD")
        kwargs.setdefault("resizable", True)
        super().__init__(*args, **kwargs)

        self._bridge = bridge

        pyglet.gl.glClearColor(
            Color.BACKGROUND.red / 255,
            Color.BACKGROUND.green / 255,
            Color.BACKGROUND.blue / 255,
            1.0,
        )

        self._batch = pyglet.graphics.Batch()
        self._g_bg   = pyglet.graphics.Group(order=0)
        self._g_bar  = pyglet.graphics.Group(order=1)
        self._g_text = pyglet.graphics.Group(order=2)

        self.layout = Layout(self.width, self.height)

        self._last_snapshot = None

        # FPS
        self._fps = 0.0
        self._fps_acc = 0.0
        self._fps_frames = 0
        self._fps_label = pyglet.text.Label(
            "", font_name="Courier New", font_size=8,
            x=6, y=6, color=(80, 80, 100, 200),
            batch=self._batch, group=self._g_text,
        )

        pyglet.clock.schedule_interval(self._tick, 1 / 30)

    # ------------------------------------------------------------------
    # Фабричные методы для групп/батча — панели используют их
    # ------------------------------------------------------------------

    @property
    def batch(self) -> pyglet.graphics.Batch:
        return self._batch

    @property
    def group_bg(self):
        return self._g_bg

    @property
    def group_bar(self):
        return self._g_bar

    @property
    def group_text(self):
        return self._g_text

    # ------------------------------------------------------------------
    # Pyglet callbacks
    # ------------------------------------------------------------------

    def on_draw(self):
        self.clear()
        self._batch.draw()
        # LogPanel использует отдельный батч (перестраивается по dirty-флагу)
        from ui.layout import Slot
        log = self.layout.get_panel(Slot.BOTTOM)
        if log is not None:
            log.draw()

    def on_resize(self, w, h):
        super().on_resize(w, h)
        self.layout.on_resize(w, h)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        from ui.layout import Slot
        log = self.layout.get_panel(Slot.BOTTOM)
        if log is not None and log.contains(x, y):
            log.on_scroll(int(scroll_y))

    # ------------------------------------------------------------------
    # Tick
    # ------------------------------------------------------------------

    def _tick(self, dt: float):
        self._fps_acc += dt
        self._fps_frames += 1
        if self._fps_acc >= 0.5:
            self._fps = self._fps_frames / self._fps_acc
            self._fps_acc = 0.0
            self._fps_frames = 0
        self._fps_label.text = f"FPS {self._fps:.0f}"

        snapshot = self._bridge.latest_snapshot()
        if snapshot is None or snapshot is self._last_snapshot:
            return
        self._last_snapshot = snapshot
        self.layout.update(snapshot, dt)