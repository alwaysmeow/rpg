import re
import threading
import pyglet

BACKGROUND_COLOR = (18, 18, 18, 255)
TEXT_COLOR = (220, 220, 220, 255)
FONT_SIZE = 25
LINE_HEIGHT = 30
PADDING = 12
MAX_LINES = 500

class LogWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lines: list[str] = []
        self._lock = threading.Lock()
        self._batch = pyglet.graphics.Batch()
        self._labels: list[pyglet.text.Label] = []
        self._scroll_offset = 0
        self._dirty = False

        pyglet.gl.glClearColor(
            BACKGROUND_COLOR[0] / 255,
            BACKGROUND_COLOR[1] / 255,
            BACKGROUND_COLOR[2] / 255,
            1.0,
        )

        pyglet.clock.schedule_interval(self._tick, 1 / 30)

    def _tick(self, dt):
        # Called on main thread by pyglet — safe to trigger redraw here
        if self._dirty:
            self._rebuild_labels()

    def push_line(self, text: str):
        clean = re.sub(r'\[/?[^\]]*\]', '', text)
        with self._lock:
            for line in clean.splitlines():
                self._lines.append(line)
            if len(self._lines) > MAX_LINES:
                self._lines = self._lines[-MAX_LINES:]
            self._dirty = True

    def _rebuild_labels(self):
        with self._lock:
            self._batch = pyglet.graphics.Batch()
            self._labels = []

            visible_lines = (self.height - 2 * PADDING) // LINE_HEIGHT
            total = len(self._lines)

            start = max(0, total - visible_lines - self._scroll_offset)
            end = max(0, total - self._scroll_offset)
            slice_ = self._lines[start:end]

            for i, text in enumerate(reversed(slice_)):
                y = PADDING + i * LINE_HEIGHT
                self._labels.append(pyglet.text.Label(
                    text,
                    font_name="Courier New",
                    font_size=FONT_SIZE,
                    color=TEXT_COLOR,
                    x=PADDING,
                    y=y,
                    batch=self._batch,
                ))

            self._dirty = False

    def on_draw(self):
        self.clear()
        self._batch.draw()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self._dirty = True

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self._scroll_offset = max(0, self._scroll_offset + int(scroll_y) * 3)
        visible_lines = (self.height - 2 * PADDING) // LINE_HEIGHT
        max_offset = max(0, len(self._lines) - visible_lines)
        self._scroll_offset = min(self._scroll_offset, max_offset)
        self._dirty = True

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
    
    def sink(self, text):
        self.push_line(str(text))