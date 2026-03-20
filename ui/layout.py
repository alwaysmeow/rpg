from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.panel import Panel


class Slot(Enum):
    LEFT   = auto()
    RIGHT  = auto()
    CENTER = auto()
    BOTTOM = auto()
    TOP    = auto()


# Фиксированная ширина боковых колонок
SIDE_W = 200

# CENTER гарантированно получает не меньше этого
CENTER_MIN_W = 300

# Фиксированные размеры для TOP/BOTTOM
TOP_H    = 50
BOTTOM_H = 120

MARGIN = 12


class Layout:
    """
    Боковые колонки (LEFT/RIGHT) имеют фиксированную ширину SIDE_W.
    CENTER получает всё оставшееся пространство (минимум CENTER_MIN_W).
    TOP/BOTTOM — полная ширина, фиксированная высота.
    """

    def __init__(self, window_w: int, window_h: int):
        self._w = window_w
        self._h = window_h
        self._panels: dict[Slot, Panel] = {}

    # ------------------------------------------------------------------

    def add_panel(self, slot: Slot, panel: Panel) -> None:
        if slot in self._panels:
            self._panels[slot].delete()
        self._panels[slot] = panel
        self._reapply_all()

    def remove_panel(self, slot: Slot) -> None:
        panel = self._panels.pop(slot, None)
        if panel:
            panel.delete()
        self._reapply_all()

    def get_panel(self, slot: Slot) -> Panel | None:
        return self._panels.get(slot)

    # ------------------------------------------------------------------

    def update(self, snapshot, dt: float) -> None:
        for panel in self._panels.values():
            panel.update(snapshot, dt)

    def on_resize(self, w: int, h: int) -> None:
        self._w = w
        self._h = h
        self._reapply_all()

    # ------------------------------------------------------------------

    def _reapply_all(self) -> None:
        for slot in list(self._panels):
            x, y, w, h = self._rect_for(slot)
            self._panels[slot].resize(x, y, w, h)

    def _rect_for(self, slot: Slot) -> tuple[int, int, int, int]:
        W, H, M = self._w, self._h, MARGIN
        has = self._panels.__contains__

        top_h    = TOP_H    if has(Slot.TOP)    else 0
        bottom_h = BOTTOM_H if has(Slot.BOTTOM) else 0

        # Вертикальная зона для LEFT / CENTER / RIGHT
        mid_y = M + (top_h + M if has(Slot.TOP) else 0)
        mid_h = H - mid_y - (bottom_h + M if has(Slot.BOTTOM) else 0) - M

        # Горизонтальное распределение:
        # LEFT и RIGHT — фиксированная ширина SIDE_W
        # CENTER — всё оставшееся, но не меньше CENTER_MIN_W
        left_w  = SIDE_W if has(Slot.LEFT)  else 0
        right_w = SIDE_W if has(Slot.RIGHT) else 0

        left_gap  = M if has(Slot.LEFT)  else 0
        right_gap = M if has(Slot.RIGHT) else 0

        center_w = max(CENTER_MIN_W, W - 2 * M - left_w - left_gap - right_w - right_gap)
        center_x = M + left_w + left_gap

        if slot == Slot.TOP:
            return M, H - M - top_h, W - 2 * M, top_h

        if slot == Slot.BOTTOM:
            return M, M, W - 2 * M, bottom_h

        if slot == Slot.LEFT:
            return M, mid_y, left_w, mid_h

        if slot == Slot.RIGHT:
            return W - M - right_w, mid_y, right_w, mid_h

        if slot == Slot.CENTER:
            return center_x, mid_y, center_w, mid_h

        raise ValueError(f"Unknown slot: {slot}")