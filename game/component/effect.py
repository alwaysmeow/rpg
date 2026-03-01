from dataclasses import dataclass
from typing import Set

@dataclass
class EffectSource:
    entity_id: int

@dataclass  
class EffectTarget:
    entity_id: int

@dataclass
class EffectDuration:
    remaining: float | None

class Effects:
    def __init__(self, stats: Set[int] | None = None):
        self.set: Set[int] = stats if stats is not None else set()
    
    def add(self, effect_id: int):
        self.set.add(effect_id)

    def discard(self, effect_id: int):
        self.set.discard(effect_id)