from component.meter import Meter

class AbilityEffect:
    def __init__(self, effect = lambda _: None):
        self.effect = effect

class Owner:
    def __init__(self, unit_id):
        self.unit_id = unit_id

class Cooldown(Meter): 
    # value = 1 - ability is ready
    pass