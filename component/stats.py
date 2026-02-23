from typing import Set

from component.stat import Stat
from component.meter import Meter

class Armor(Stat): formula_key = "armor"
class MagicResistance(Stat): formula_key = "magic_resistance"
class AttackDamage(Stat): formula_key = "attack_damage"
class AttackSpeed(Stat): formula_key = "attack_speed"
class AttackDelay(Stat): formula_key = "attack_delay"

class Health(Meter): formula_key = "health"
class Mana(Meter): formula_key = "mana"

class Stats:
    def __init__(self, stats: Set[type] | None = None):
        self.set: Set[type] = stats if stats is not None else set()
    
    def add(self, stat: type):
        self.set.add(stat)

    def discard(self, stat: type):
        self.set.discard(stat)