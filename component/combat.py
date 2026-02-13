from typing import List

class CombatParticipants:
    def __init__(self, team1: List[int], team2: List[int]):
        self.team1 = team1
        self.team2 = team2

class CombatState:
    def __init__(self):
        self.active = True
        self.winner = None