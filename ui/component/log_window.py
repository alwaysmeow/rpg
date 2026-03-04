from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, RichLog


class LogWindow(Vertical):
    def __init__(self, logger):
        super().__init__()
        logger.sink = self.write

    def compose(self) -> ComposeResult:
        yield Static("Combat Log", classes="log-title")
        yield RichLog(highlight=True, markup=True, wrap=True, id="log")

    def write(self, text):
        self.query_one("#log", RichLog).write(text)