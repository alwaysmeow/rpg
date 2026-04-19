from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

from ui.hud_constants import (
    CENTER_MAX_H,
    CENTER_MAX_W,
    CENTER_MIN_H,
    CENTER_MIN_W,
    LOG_MAX_H,
    LOG_MIN_H,
    SIDE_PANEL_MAX_W,
    SIDE_PANEL_MIN_W,
    STATS_MAX_H,
    STATS_MIN_H,
    WINDOW_MARGIN,
)

if TYPE_CHECKING:
    from ui.panel import Panel


class Slot(Enum):
    LEFT   = auto()
    RIGHT  = auto()
    CENTER = auto()
    BOTTOM = auto()
    TOP    = auto()


class Layout:
    """
    CENTER — статичная сцена боя по центру окна.
    LEFT/RIGHT — плавающие HUD-окна поверх сцены; их размеры не влияют
    на положение центральной панели.
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
        W, H, M = self._w, self._h, WINDOW_MARGIN
        top_y = H - M

        if slot == Slot.CENTER:
            center_w = _clamp(int(W * 0.60), CENTER_MIN_W, CENTER_MAX_W)
            center_h = _clamp(int(H * 0.40), CENTER_MIN_H, CENTER_MAX_H)
            center_x = (W - center_w) // 2
            center_y = top_y - center_h
            return center_x, center_y, center_w, center_h

        if slot == Slot.LEFT:
            width = _clamp(int(W * 0.24), SIDE_PANEL_MIN_W, SIDE_PANEL_MAX_W)
            height = _clamp(int(H * 0.62), LOG_MIN_H, LOG_MAX_H)
            return M, top_y - height, width, height

        if slot == Slot.RIGHT:
            width = _clamp(int(W * 0.24), SIDE_PANEL_MIN_W, SIDE_PANEL_MAX_W)
            height = _clamp(int(H * 0.40), STATS_MIN_H, STATS_MAX_H)
            x = W - M - width
            y = top_y - height
            return x, y, width, height

        if slot == Slot.TOP:
            return M, H - M - 50, W - 2 * M, 50

        if slot == Slot.BOTTOM:
            return M, M, W - 2 * M, 120

        raise ValueError(f"Unknown slot: {slot}")


def _clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(max_value, value))
