from textual.app import App, ComposeResult
from pathlib import Path

from ui.component.unit import Unit

class GameApp(App):
    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    CSS_PATH = list(Path(__file__).parent.glob("style/*.css"))

    def compose(self) -> ComposeResult:
        yield Unit('flaneur', 100)