import json
import pyglet

from ui.hud_window import HUDWindow
from ui.layout import Slot


class HUDRenderer:
    """
    Создаёт HUDWindow и регистрирует панели согласно конфигу.

    config/hud.json:
    {
        "width": 1100,
        "height": 580,
        "panels": ["log", "arena", "stats"]
    }

    Доступные панели:
      "arena"  → ArenaPanel в CENTER  (юниты обеих команд + таймер)
      "log"    → LogPanel   в LEFT    (лог боя)
      "stats"  → StatsPanel в RIGHT   (подробные статы первого юнита)
    """

    DEFAULT_CONFIG = {
        "width":  1100,
        "height": 580,
        "panels": ["log", "arena", "stats"],
    }

    def __init__(self, bridge=None, config_path: str = "config/hud.json"):
        self.bridge       = bridge
        self._config_path = config_path
        self._window: HUDWindow | None = None

    def run(self) -> None:
        cfg = self._load_config()
        self._window = HUDWindow(
            self.bridge,
            width=cfg["width"],
            height=cfg["height"],
        )
        self._register_panels(cfg["panels"])
        pyglet.app.run()

    # ------------------------------------------------------------------

    def _load_config(self) -> dict:
        try:
            with open(self._config_path) as f:
                return {**self.DEFAULT_CONFIG, **json.load(f)}
        except (FileNotFoundError, json.JSONDecodeError):
            return self.DEFAULT_CONFIG

    def _register_panels(self, panel_names: list[str]) -> None:
        from ui.panels.arena_panel import ArenaPanel
        from ui.panels.log_panel   import LogPanel
        from ui.panels.stats_panel import StatsPanel

        w = self._window

        builders = {
            "arena": lambda: (Slot.CENTER, ArenaPanel(
                w.batch, w.group_bg, w.group_bar, w.group_text)),
            "log":   lambda: (Slot.LEFT,   LogPanel(
                w.batch, w.group_bg, w.group_text)),
            "stats": lambda: (Slot.RIGHT,  StatsPanel(
                w.batch, w.group_bg, w.group_bar, w.group_text)),
        }

        for name in panel_names:
            if name in builders:
                slot, panel = builders[name]()
                w.layout.add_panel(slot, panel)

    def get_sink(self):
        buffer = []
        def sink(text):
            if self._window is None:
                buffer.append(str(text))
                return
            log = self._window.layout.get_panel(Slot.LEFT)
            if log is None:
                return
            # Сбрасываем буфер при первом живом вызове
            for buffered in buffer:
                log.push_line(buffered)
            buffer.clear()
            log.push_line(str(text))
        return sink