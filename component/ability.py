from component.meter import Meter

class AbilityEffect:
    def __init__(self, handler = lambda world, caster, target: None):
        self.handler = handler

class Owner:
    def __init__(self, unit_id):
        self.unit_id = unit_id

class CastTime:
    def __init__(self, value = 0):
        self.unit_id = value

class Cooldown(Meter): 
    # value = 1 - ability is ready
    pass

class Autocast:
    def __init__(self, value = False):
        self.value = value