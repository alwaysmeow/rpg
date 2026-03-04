from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from ui.component.unit import Unit


class Team(Vertical):
    def __init__(self, team_name: str, units: list[tuple[str, int]]):
        super().__init__()
        self.team_name = team_name
        self.units = units

    def compose(self) -> ComposeResult:
        yield Static(self.team_name, classes="team-name")
        for unit_name, max_hp in self.units:
            yield Unit(unit_name, max_hp)