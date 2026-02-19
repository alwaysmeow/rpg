from typing import Set

from component.stat import FormulaStat
from component.meter import FormulaMeter

class Armor(FormulaStat): pass
class MagicResist(FormulaStat): pass
class AttackDamage(FormulaStat): pass
class AttackSpeed(FormulaStat): pass

class Health(FormulaMeter): pass
class Mana(FormulaMeter): pass

class Stats:
    def __init__(self, stats: Set[type] | None = None):
        self.set: Set[type] = stats if stats is not None else set()
    
    def add(self, stat: type):
        self.set.add(stat)

    def discard(self, stat: type):
        self.set.discard(stat)