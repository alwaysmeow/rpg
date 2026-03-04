from textual.app import App, ComposeResult
from textual.containers import Vertical
from pathlib import Path

from ui.component.combat import Combat
from ui.component.log_window import LogWindow

class GameApp(App):
    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    CSS_PATH = list(Path(__file__).parent.glob("style/*.tcss"))

    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Combat([
                ("Team 1", [("flaneur", 100)]),
                ("Team 2", [("meowmeow", 100)]),
            ])
            yield LogWindow(self.logger)

    def get_log(self) -> LogWindow:
        return self.query_one(LogWindow)