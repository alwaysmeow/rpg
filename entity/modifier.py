from enum import Enum

class ModifierType(Enum):
    Flat = 0
    Multiplier = 1

class Modifier:
    def __init__(self, value, type):
        self.value = value
        self.type = type