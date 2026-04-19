import pyglet

from ui.color import Color
from ui.layout import Layout, Slot
from ui.panels.stats_panel import StatsPanel


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
        self._stats_panel: StatsPanel | None = None

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
        log = self.layout.get_panel(Slot.LEFT)
        if log is not None:
            log.draw()

    def on_resize(self, w, h):
        super().on_resize(w, h)
        self.layout.on_resize(w, h)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        log = self.layout.get_panel(Slot.LEFT)
        if log is not None and log.contains(x, y):
            log.on_scroll(int(scroll_y))

    def on_mouse_press(self, x, y, button, modifiers):
        if button != pyglet.window.mouse.RIGHT:
            return

        arena = self.layout.get_panel(Slot.CENTER)
        if arena is None or not hasattr(arena, "unit_at"):
            return

        unit_id = arena.unit_at(x, y)
        if unit_id is None:
            return

        self._toggle_stats_panel(unit_id)

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

    def _toggle_stats_panel(self, unit_id: int) -> None:
        stats = self._get_stats_panel()
        if stats is None:
            return

        if self.layout.get_panel(Slot.RIGHT) is not None and stats.selected_id == unit_id:
            stats.deselect()
            self.layout.remove_panel(Slot.RIGHT)
            return

        stats.select(unit_id)
        if self.layout.get_panel(Slot.RIGHT) is None:
            self.layout.add_panel(Slot.RIGHT, stats)

    def _get_stats_panel(self) -> StatsPanel | None:
        if self._stats_panel is not None:
            return self._stats_panel

        existing = self.layout.get_panel(Slot.RIGHT)
        if isinstance(existing, StatsPanel):
            self._stats_panel = existing
            return existing

        self._stats_panel = StatsPanel(
            self.batch,
            self.group_bg,
            self.group_bar,
            self.group_text,
        )
        return self._stats_panel
