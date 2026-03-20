import re
import threading
import pyglet

from ui.panel import Panel

FONT_SIZE   = 20
LINE_HEIGHT = 25
PADDING     = 15
MAX_LINES   = 500
TEXT_COLOR  = (0, 0, 0, 220)


class LogPanel(Panel):
    """
    Панель лога: прокручиваемый список строк.

    push_line(text) потокобезопасен — можно вызывать из симуляции.
    Скролл колесом мыши работает только когда курсор над панелью
    (проверку делает HUDWindow через on_mouse_scroll).
    """

    def __init__(self, batch, group_bg, group_text):
        self._batch_ref = batch         # храним ссылку, но лейблы в своём батче
        self._log_batch = pyglet.graphics.Batch()
        self._g_text    = group_text

        self._lines: list[str] = []
        self._labels: list[pyglet.text.Label] = []
        self._scroll_offset = 0
        self._dirty = False
        self._lock  = threading.Lock()

        self._x = self._y = self._w = self._h = 0

    # ------------------------------------------------------------------
    # Panel interface
    # ------------------------------------------------------------------

    def resize(self, x: int, y: int, w: int, h: int) -> None:
        self._x, self._y, self._w, self._h = x, y, w, h
        self._dirty = True

    def update(self, snapshot, dt: float) -> None:
        # Лог не читает снапшот — он наполняется через push_line
        if self._dirty:
            self._rebuild_labels()

    def delete(self) -> None:
        self._labels.clear()
        self._log_batch = pyglet.graphics.Batch()

    # ------------------------------------------------------------------
    # Публичный API
    # ------------------------------------------------------------------

    def push_line(self, text: str) -> None:
        clean = re.sub(r'\[/?[^\]]*\]', '', str(text))
        with self._lock:
            for line in clean.splitlines():
                self._lines.append(line)
            if len(self._lines) > MAX_LINES:
                self._lines = self._lines[-MAX_LINES:]
            self._dirty = True

    def on_scroll(self, scroll_y: int) -> None:
        """Вызывается из HUDWindow.on_mouse_scroll если курсор над панелью."""
        visible = max(1, (self._h - 2 * PADDING) // LINE_HEIGHT)
        max_off = max(0, len(self._lines) - visible)
        self._scroll_offset = max(0, min(max_off, self._scroll_offset + scroll_y * 3))
        self._dirty = True

    def contains(self, px: int, py: int) -> bool:
        return (self._x <= px <= self._x + self._w and
                self._y <= py <= self._y + self._h)

    def draw(self) -> None:
        """Вызывается из HUDWindow.on_draw отдельно (свой батч)."""
        self._log_batch.draw()

    # ------------------------------------------------------------------

    def _rebuild_labels(self) -> None:
        with self._lock:
            self._log_batch = pyglet.graphics.Batch()
            self._labels = []

            visible = max(1, (self._h - 2 * PADDING) // LINE_HEIGHT)
            total   = len(self._lines)
            start   = max(0, total - visible - self._scroll_offset)
            end     = max(0, total - self._scroll_offset)

            for i, text in enumerate(reversed(self._lines[start:end])):
                lx = self._x + PADDING
                ly = self._y + PADDING + i * LINE_HEIGHT
                if ly + LINE_HEIGHT > self._y + self._h:
                    break
                self._labels.append(pyglet.text.Label(
                    text,
                    font_name="Courier New", font_size=FONT_SIZE,
                    color=TEXT_COLOR,
                    x=lx, y=ly,
                    batch=self._log_batch,
                ))

            self._dirty = False
