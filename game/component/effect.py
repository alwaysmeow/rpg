from dataclasses import dataclass

@dataclass
class EffectSource:
    entity_id: int

@dataclass  
class EffectTarget:
    entity_id: int

@dataclass
class EffectDuration:
    remaining: float

class EffectBehaviour:
    def on_apply(self, world, effect_id): pass
    def on_remove(self, world, effect_id): pass

class CompositeEffect(EffectBehaviour):
    def __init__(self, *behaviours: EffectBehaviour):
        self.behaviours = behaviours

    def on_apply(self, world, effect_id):
        for b in self.behaviours:
            b.on_apply(world, effect_id)

    def on_remove(self, world, effect_id):
        for b in self.behaviours:
            b.on_remove(world, effect_id)