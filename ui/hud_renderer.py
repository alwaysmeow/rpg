import json
import pyglet

from ui.hud_window import HUDWindow
from ui.layout import Slot


class HUDRenderer:
    """
    Создаёт HUDWindow и регистрирует панели согласно конфигу.

    config/hud.json:
    {
        "width": 900,
        "height": 520,
        "panels": ["arena", "log"]
    }

    Доступные панели:
      "arena"  → ArenaPanel в CENTER (юниты обеих команд + таймер)
      "log"    → LogPanel   в BOTTOM
      (LEFT / RIGHT зарезервированы под будущие панели)
    """

    DEFAULT_CONFIG = {
        "width":  900,
        "height": 520,
        "panels": ["arena", "log"],
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

        w = self._window

        builders = {
            "arena": lambda: (Slot.CENTER, ArenaPanel(
                w.batch, w.group_bg, w.group_bar, w.group_text)),
            "log":   lambda: (Slot.BOTTOM, LogPanel(
                w.batch, w.group_bg, w.group_text)),
        }

        for name in panel_names:
            if name in builders:
                slot, panel = builders[name]()
                w.layout.add_panel(slot, panel)

    def get_sink(self):
        def sink(text):
            if self._window is None:
                return
            log = self._window.layout.get_panel(Slot.BOTTOM)
            if log is not None:
                log.push_line(str(text))
        return sink