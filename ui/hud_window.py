import pyglet

from ui.color import Color
from ui.layout import Layout, Slot
from ui.panels.arena_panel import ArenaPanel
from ui.panels.log_panel import LogPanel
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
        self._log_panel: LogPanel | None = None
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
        log = self.layout.get_panel(Slot.LEFT)
        if log is not None:
            log.draw()

    def on_resize(self, w, h):
        super().on_resize(w, h)
        self.layout.on_resize(w, h)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
        elif symbol == pyglet.window.key.TAB:
            self.toggle_log_panel()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        log = self.layout.get_panel(Slot.LEFT)
        if log is not None and log.contains(x, y):
            log.on_scroll(int(scroll_y))

    def on_mouse_press(self, x, y, button, modifiers):
        log = self.layout.get_panel(Slot.LEFT)
        if log is not None and log.on_mouse_press(x, y, button, modifiers):
            return

        if button != pyglet.window.mouse.RIGHT:
            return

        arena = self.layout.get_panel(Slot.CENTER)
        if not isinstance(arena, ArenaPanel):
            return

        unit_id = arena.unit_at(x, y)
        if unit_id is None:
            return

        self._toggle_stats_panel(unit_id)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        log = self.layout.get_panel(Slot.LEFT)
        if log is not None and log.on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            return

    def on_mouse_release(self, x, y, button, modifiers):
        log = self.layout.get_panel(Slot.LEFT)
        if log is not None and log.on_mouse_release(x, y, button, modifiers):
            return

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
        if snapshot is not None:
            self._last_snapshot = snapshot

        self.layout.update(self._last_snapshot, dt)

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

    def append_log_line(self, text: str) -> None:
        self._get_log_panel().push_line(text)

    def toggle_log_panel(self) -> None:
        if self.layout.get_panel(Slot.LEFT) is None:
            self.layout.add_panel(Slot.LEFT, self._get_log_panel())
        else:
            self.layout.remove_panel(Slot.LEFT)

    def _get_log_panel(self) -> LogPanel:
        if self._log_panel is not None:
            return self._log_panel

        existing = self.layout.get_panel(Slot.LEFT)
        if isinstance(existing, LogPanel):
            self._log_panel = existing
            return existing

        self._log_panel = LogPanel(
            self.batch,
            self.group_bg,
            self.group_text,
        )
        return self._log_panel
