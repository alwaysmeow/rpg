from textual.app import App, ComposeResult
from textual.widgets import Static, ProgressBar
from textual.containers import Horizontal
from textual.reactive import reactive


class ResourceBar(Horizontal):
    def __init__(self, value, max_value, bar_classes, id=None):
        super().__init__()
        
        self.id = id
        self.value = value
        self.max_value = max_value
        self.bar_classes = bar_classes

    def compose(self) -> ComposeResult:
        yield ProgressBar(
            total=self.max_value,
            id=self.id,
            classes=self.bar_classes,
            show_eta=False,
            show_percentage=False
        )

        yield Static(f"{self.value} / {self.max_value}")

    def on_mount(self) -> None:
        self.update_hp()

    def update_hp(self):
        bar = self.query_one(f"#{self.id}", ProgressBar)
        bar.progress = self.value