class CombatParticipation:
    def __init__(self, combat_id, team_index):
        self.combat_id = combat_id
        self.team_index = team_index

class CombatState:
    def __init__(self):
        self.active = True
        self.winner = None