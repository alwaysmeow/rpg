class AbilityEffect:
    def __init__(self, effect = lambda _: None):
        self.effect = effect

class Owner:
    def __init__(self, unit_id):
        self.unit_id = unit_id

class Cooldown:
    def __init__(self, duration = 0):
        self.duration = duration
        self.value = duration