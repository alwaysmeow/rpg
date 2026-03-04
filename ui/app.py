from textual.app import App, ComposeResult
from pathlib import Path

from ui.component.combat import Combat

class GameApp(App):
    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    CSS_PATH = list(Path(__file__).parent.glob("style/*.css"))

    def compose(self) -> ComposeResult:
        yield Combat([
            ("Team 1", [("Flaneur", 100), ("Rogue", 80)]),
            ("Team 2", [("Guard", 120), ("Mage", 70)]),
        ])