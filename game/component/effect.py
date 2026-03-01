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

class EffectBehaviour:
    def on_apply(self, world, effect_id): pass
    def on_tick(self, world, effect_id): pass
    def on_remove(self, world, effect_id): pass

class CompositeBehaviour(EffectBehaviour):
    def __init__(self, *behaviours: EffectBehaviour):
        self.behaviours = behaviours

    def on_apply(self, world, effect_id):
        for b in self.behaviours:
            b.on_apply(world, effect_id)

    def on_tick(self, world, effect_id):
        for b in self.behaviours:
            b.on_tick(world, effect_id)

    def on_remove(self, world, effect_id):
        for b in self.behaviours:
            b.on_remove(world, effect_id)