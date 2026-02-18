from enum import Enum

# TODO: color from config

class DamageType(Enum):
    Pure = ("Pure", "yellow")
    Physical = ("Physical", "red")
    Magic = ("Magic", "blue")

    def __init__(self, value, color):
        self._value_ = value
        self.color = color