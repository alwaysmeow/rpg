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


# CENTER гарантированно получает не меньше этого
CENTER_MIN_W = 400

# Фиксированные размеры для TOP/BOTTOM
TOP_H    = 50
BOTTOM_H = 120

# Боковые колонки: если нет явного размера — берут остаток поровну
SIDE_MIN_W = 160

MARGIN = 12


class Layout:
    """
    Приоритет: CENTER получает CENTER_MIN_W или больше.
    LEFT/RIGHT делят оставшееся пространство поровну.
    TOP/BOTTOM — полная ширина, фиксированная высота.

    Добавление/удаление панели пересчитывает геометрию всех слотов.
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
        # CENTER получает max(CENTER_MIN_W, остаток после боковых)
        # Боковые делят то, что осталось после CENTER
        total_side_w = W - 2 * M - CENTER_MIN_W - (
            M if has(Slot.LEFT) else 0) - (M if has(Slot.RIGHT) else 0)

        n_sides = (1 if has(Slot.LEFT) else 0) + (1 if has(Slot.RIGHT) else 0)

        if n_sides > 0:
            side_w = max(SIDE_MIN_W, total_side_w // n_sides)
        else:
            side_w = 0

        center_w = W - 2 * M \
            - (side_w + M if has(Slot.LEFT) else 0) \
            - (side_w + M if has(Slot.RIGHT) else 0)

        center_x = M + (side_w + M if has(Slot.LEFT) else 0)

        if slot == Slot.TOP:
            return M, H - M - top_h, W - 2 * M, top_h

        if slot == Slot.BOTTOM:
            return M, M, W - 2 * M, bottom_h

        if slot == Slot.LEFT:
            return M, mid_y, side_w, mid_h

        if slot == Slot.RIGHT:
            return W - M - side_w, mid_y, side_w, mid_h

        if slot == Slot.CENTER:
            return center_x, mid_y, center_w, mid_h

        raise ValueError(f"Unknown slot: {slot}")