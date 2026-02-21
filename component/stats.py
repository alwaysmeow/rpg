from typing import Set

from component.stat import FormulaStat
from component.meter import FormulaMeter

class Armor(FormulaStat): formula_key = "armor"
class MagicResistance(FormulaStat): formula_key = "magic_resistance"
class AttackDamage(FormulaStat): formula_key = "attack_damage"
class AttackSpeed(FormulaStat): formula_key = "attack_speed"
class AttackDelay(FormulaStat): formula_key = "attack_delay"

class Health(FormulaMeter): formula_key = "health"
class Mana(FormulaMeter): formula_key = "mana"

class Stats:
    def __init__(self, stats: Set[type] | None = None):
        self.set: Set[type] = stats if stats is not None else set()
    
    def add(self, stat: type):
        self.set.add(stat)

    def discard(self, stat: type):
        self.set.discard(stat)