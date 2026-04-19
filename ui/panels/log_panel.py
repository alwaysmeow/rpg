import re
import threading
import pyglet
from pyglet import shapes

from ui.hud_constants import FONT_NAME, PANEL_BODY_FONT_SIZE, PANEL_TITLE_FONT_SIZE
from ui.panel import Panel

FONT_SIZE   = PANEL_BODY_FONT_SIZE
LINE_HEIGHT = 34
PADDING     = 15
MAX_LINES   = 500
TEXT_COLOR  = (0, 0, 0, 220)
TITLE_H     = 30
WINDOW_BG   = (243, 235, 232)
WINDOW_BAR  = (217, 208, 204)
WINDOW_EDGE = (188, 174, 170)
WINDOW_SHADOW = (65, 45, 40, 38)
CONTENT_PAD_X = 14
CONTENT_PAD_Y = 12
SCROLLBAR_W = 10
SCROLLBAR_GAP = 10
SCROLLBAR_MIN_H = 28
CONTENT_BG = (250, 246, 244)
CONTENT_EDGE = (222, 212, 208)
SCROLL_TRACK = (228, 220, 216)
SCROLL_THUMB = (174, 162, 156)
SCROLL_THUMB_ACTIVE = (145, 132, 126)
TEXT_RIGHT_PAD = 8


class LogPanel(Panel):
    """
    Панель лога: прокручиваемый список строк.

    push_line(text) потокобезопасен — можно вызывать из симуляции.
    Скролл колесом мыши работает только когда курсор над панелью
    (проверку делает HUDWindow через on_mouse_scroll).
    """

    def __init__(self, batch, group_bg, group_text):
        self._batch_ref = batch
        self._log_batch = pyglet.graphics.Batch()
        self._g_bg      = group_bg
        self._g_text    = group_text

        self._lines: list[str] = []
        self._wrapped_lines: list[str] = []
        self._labels: list[pyglet.text.Label] = []
        self._scroll_offset = 0
        self._dirty = False
        self._lock  = threading.Lock()
        self._dragging_scrollbar = False
        self._scrollbar_drag_dy = 0.0
        self._text_width_cache: dict[str, int] = {}

        self._x = self._y = self._w = self._h = 0
        self._shadow: shapes.RoundedRectangle | None = None
        self._bg: shapes.RoundedRectangle | None = None
        self._title_bar: shapes.RoundedRectangle | None = None
        self._title_label: pyglet.text.Label | None = None
        self._content_bg: shapes.Rectangle | None = None
        self._scroll_track: shapes.RoundedRectangle | None = None
        self._scroll_thumb: shapes.RoundedRectangle | None = None

    # ------------------------------------------------------------------
    # Panel interface
    # ------------------------------------------------------------------

    def resize(self, x: int, y: int, w: int, h: int) -> None:
        self._x, self._y, self._w, self._h = x, y, w, h
        self._rebuild_frame()
        self._dirty = True

    def update(self, snapshot, dt: float) -> None:
        # Лог не читает снапшот — он наполняется через push_line
        if self._dirty:
            self._rebuild_labels()

    def delete(self) -> None:
        for obj in (self._shadow, self._bg, self._title_bar, self._title_label,
                    self._content_bg, self._scroll_track, self._scroll_thumb):
            if obj:
                obj.delete()
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
        visible = self._visible_lines()
        max_off = max(0, len(self._wrapped_lines) - visible)
        self._scroll_offset = max(0, min(max_off, self._scroll_offset - scroll_y * 3))
        self._dirty = True

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool:
        if button != pyglet.window.mouse.LEFT or not self.contains(x, y):
            return False

        if self._scroll_thumb is not None and self._thumb_contains(x, y):
            self._dragging_scrollbar = True
            self._scrollbar_drag_dy = y - self._scroll_thumb.y
            self._update_scrollbar_visual()
            return True

        if self._scroll_track is not None and self._track_contains(x, y):
            self._set_scroll_from_thumb_center(y)
            self._dragging_scrollbar = True
            self._scrollbar_drag_dy = self._scroll_thumb.height / 2 if self._scroll_thumb else 0
            self._update_scrollbar_visual()
            return True

        return False

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int) -> bool:
        if not self._dragging_scrollbar:
            return False

        self._set_scroll_from_thumb_bottom(y - self._scrollbar_drag_dy)
        self._update_scrollbar_visual()
        return True

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> bool:
        if not self._dragging_scrollbar:
            return False

        self._dragging_scrollbar = False
        self._update_scrollbar_visual()
        return True

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
            self._wrapped_lines = self._build_wrapped_lines()

            visible = self._visible_lines()
            total   = len(self._wrapped_lines)
            start   = max(0, total - visible - self._scroll_offset)
            end     = max(0, total - self._scroll_offset)

            visible_lines = self._wrapped_lines[start:end]
            for row, text in enumerate(visible_lines):
                lx = self._content_x()
                ly = self._content_top() - (row + 1) * LINE_HEIGHT
                if ly < self._content_y():
                    break
                self._labels.append(pyglet.text.Label(
                    text,
                    font_name=FONT_NAME, font_size=FONT_SIZE,
                    color=TEXT_COLOR,
                    x=lx, y=ly,
                    batch=self._log_batch,
                ))

            self._clamp_scroll_offset()
            self._update_scrollbar_visual()
            self._dirty = False

    def _visible_lines(self) -> int:
        text_h = max(1, self._content_h())
        return max(1, text_h // LINE_HEIGHT)

    def _build_wrapped_lines(self) -> list[str]:
        wrapped: list[str] = []
        for line in self._lines:
            wrapped.extend(self._wrap_line(line))
        return wrapped[-MAX_LINES:]

    def _content_x(self) -> int:
        return self._x + CONTENT_PAD_X

    def _content_y(self) -> int:
        return self._y + CONTENT_PAD_Y

    def _content_w(self) -> int:
        return max(40, self._w - CONTENT_PAD_X * 2 - SCROLLBAR_W - SCROLLBAR_GAP)

    def _max_text_w(self) -> int:
        return max(24, self._content_w() - TEXT_RIGHT_PAD)

    def _content_h(self) -> int:
        return max(40, self._h - TITLE_H - CONTENT_PAD_Y * 2 - 8)

    def _content_top(self) -> int:
        return self._content_y() + self._content_h()

    def _track_x(self) -> int:
        return self._content_x() + self._content_w() + SCROLLBAR_GAP

    def _track_y(self) -> int:
        return self._content_y()

    def _track_h(self) -> int:
        return self._content_h()

    def _thumb_contains(self, px: int, py: int) -> bool:
        thumb = self._scroll_thumb
        return bool(
            thumb is not None and
            thumb.x <= px <= thumb.x + thumb.width and
            thumb.y <= py <= thumb.y + thumb.height
        )

    def _track_contains(self, px: int, py: int) -> bool:
        track = self._scroll_track
        return bool(
            track is not None and
            track.x <= px <= track.x + track.width and
            track.y <= py <= track.y + track.height
        )

    def _clamp_scroll_offset(self) -> None:
        max_off = max(0, len(self._wrapped_lines) - self._visible_lines())
        self._scroll_offset = max(0, min(max_off, self._scroll_offset))

    def _set_scroll_from_thumb_center(self, center_y: float) -> None:
        if self._scroll_thumb is None:
            return
        self._set_scroll_from_thumb_bottom(center_y - self._scroll_thumb.height / 2)

    def _set_scroll_from_thumb_bottom(self, thumb_y: float) -> None:
        if self._scroll_thumb is None:
            return

        max_off = max(0, len(self._wrapped_lines) - self._visible_lines())
        travel = max(1, self._track_h() - self._scroll_thumb.height)
        clamped_y = max(self._track_y(), min(self._track_y() + travel, thumb_y))
        ratio = (clamped_y - self._track_y()) / travel
        self._scroll_offset = int(round(ratio * max_off))
        self._dirty = True

    def _update_scrollbar_visual(self) -> None:
        if self._scroll_track is None or self._scroll_thumb is None:
            return

        max_off = max(0, len(self._wrapped_lines) - self._visible_lines())
        visible = self._visible_lines()
        total = max(visible, len(self._wrapped_lines))
        track_h = self._track_h()

        thumb_h = track_h if max_off == 0 else max(
            SCROLLBAR_MIN_H,
            int(track_h * (visible / total)),
        )
        self._scroll_thumb.height = min(track_h, thumb_h)

        travel = max(0, track_h - self._scroll_thumb.height)
        ratio = 0 if max_off == 0 else self._scroll_offset / max_off
        self._scroll_thumb.y = self._track_y() + int(travel * ratio)
        self._scroll_thumb.color = (
            SCROLL_THUMB_ACTIVE if self._dragging_scrollbar else SCROLL_THUMB
        )
        self._scroll_thumb.opacity = 255 if max_off > 0 else 120

    def _rebuild_frame(self) -> None:
        for obj in (self._shadow, self._bg, self._title_bar, self._title_label,
                    self._content_bg, self._scroll_track, self._scroll_thumb):
            if obj:
                obj.delete()

        x, y, w, h = self._x, self._y, self._w, self._h
        if w < 10 or h < 10:
            self._shadow = self._bg = self._title_bar = self._title_label = None
            self._content_bg = self._scroll_track = self._scroll_thumb = None
            return

        self._shadow = shapes.RoundedRectangle(
            x + 4, y - 4, w, h, radius=12,
            color=WINDOW_SHADOW[:3], batch=self._batch_ref, group=self._g_bg,
        )
        self._shadow.opacity = WINDOW_SHADOW[3]

        self._bg = shapes.RoundedRectangle(
            x, y, w, h, radius=12,
            color=WINDOW_BG, batch=self._batch_ref, group=self._g_bg,
        )
        self._bg.opacity = 238

        self._title_bar = shapes.RoundedRectangle(
            x, y + h - TITLE_H, w, TITLE_H, radius=12,
            color=WINDOW_BAR, batch=self._batch_ref, group=self._g_bg,
        )
        self._title_bar.opacity = 248

        self._title_label = pyglet.text.Label(
            "Combat Log",
            font_name=FONT_NAME, font_size=PANEL_TITLE_FONT_SIZE,
            x=x + PADDING, y=y + h - TITLE_H // 2,
            anchor_y="center",
            color=(*WINDOW_EDGE, 255),
            batch=self._batch_ref, group=self._g_text,
        )

        self._content_bg = shapes.Rectangle(
            self._content_x() - 4, self._content_y() - 4,
            self._content_w() + SCROLLBAR_W + SCROLLBAR_GAP + 8,
            self._content_h() + 8,
            color=CONTENT_BG, batch=self._batch_ref, group=self._g_bg,
        )
        self._content_bg.opacity = 245

        self._scroll_track = shapes.RoundedRectangle(
            self._track_x(), self._track_y(),
            SCROLLBAR_W, self._track_h(),
            radius=4,
            color=SCROLL_TRACK, batch=self._batch_ref, group=self._g_bg,
        )
        self._scroll_track.opacity = 255

        self._scroll_thumb = shapes.RoundedRectangle(
            self._track_x(), self._track_y(),
            SCROLLBAR_W, self._track_h(),
            radius=4,
            color=SCROLL_THUMB, batch=self._batch_ref, group=self._g_bg,
        )
        self._scroll_thumb.opacity = 120
        self._update_scrollbar_visual()

    def _wrap_line(self, line: str) -> list[str]:
        if not line:
            return [""]

        max_width = self._max_text_w()
        chunks = re.findall(r"\S+\s*", line)
        wrapped: list[str] = []
        current = ""

        for chunk in chunks:
            candidate = current + chunk
            if current and self._measure_text_width(candidate.rstrip()) > max_width:
                wrapped.append(current.rstrip())
                current = chunk.lstrip()
                if self._measure_text_width(current.rstrip()) > max_width:
                    wrapped.extend(self._break_long_chunk(current.rstrip(), max_width))
                    current = ""
            else:
                current = candidate

        if current or not wrapped:
            if self._measure_text_width(current.rstrip()) <= max_width:
                wrapped.append(current.rstrip())
            else:
                wrapped.extend(self._break_long_chunk(current.rstrip(), max_width))

        return wrapped or [""]

    def _break_long_chunk(self, chunk: str, max_width: int) -> list[str]:
        if not chunk:
            return [""]

        parts: list[str] = []
        current = ""
        for char in chunk:
            candidate = current + char
            if current and self._measure_text_width(candidate) > max_width:
                parts.append(current)
                current = char
            else:
                current = candidate
        if current:
            parts.append(current)
        return parts

    def _measure_text_width(self, text: str) -> float:
        if not text:
            return 0.0

        cached = self._text_width_cache.get(text)
        if cached is not None:
            return float(cached)

        label = pyglet.text.Label(
            text,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
        )
        width = int(label.content_width)
        self._text_width_cache[text] = width
        return float(width)
