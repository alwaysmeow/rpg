from textual.app import ComposeResult
from textual.containers import Horizontal

from ui.component.team import Team


class Combat(Horizontal):
    def __init__(self, teams: list[tuple[str, list]]):
        super().__init__()
        self.teams = teams

    def compose(self) -> ComposeResult:
        for team_name, units in self.teams:
            yield Team(team_name, units)