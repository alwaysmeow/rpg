from enum import Enum

from utils import load_config

# TODO: do something with this config loading
config = load_config("config/ui.json")

class DamageType(Enum):
    Pure = ("Pure", config["pure_damage_color"] or "yellow")
    Physical = ("Physical", config["physical_damage_color"] or "red")
    Magic = ("Magic", config["magic_damage_color"] or "blue")

    def __init__(self, value, color):
        self._value_ = value
        self.color = color