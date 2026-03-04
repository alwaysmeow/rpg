from textual.app import ComposeResult
from textual.widgets import Static, ProgressBar
from textual.containers import Vertical
from textual.reactive import reactive

from ui.component.resource_bar import ResourceBar

class Unit(Vertical):
    hp = reactive(80)

    def __init__(self, unit_name: str, max_hp: int = 100):
        super().__init__()
        self.unit_name = unit_name
        self.max_hp = max_hp

    def compose(self) -> ComposeResult:
        yield Static(self.unit_name, classes="unit-name")
        yield ResourceBar(80, self.max_hp, "health", "id1")
        yield ResourceBar(80, 100, "mana", "id2")
        yield ResourceBar(80, 100, "stamina", "id3")