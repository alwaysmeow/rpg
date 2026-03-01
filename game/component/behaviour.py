def _composite_method(name):
    def method(self, world, entity_id):
        for b in self.behaviours:
            getattr(b, name)(world, entity_id)
    method.__name__ = name
    return method

class Behaviour:
    # Effect behaviours
    def on_apply(self, world, entity_id): pass
    def on_tick(self, world, entity_id): pass
    def on_remove(self, world, entity_id): pass

    # Ability behaviours
    def on_attack(self, world, effect_id): pass
    def on_cast(self, world, effect_id): pass
    def on_cast_end(self, world, effect_id): pass

class CompositeBehaviour(Behaviour):
    def __init__(self, *behaviours: Behaviour):
        self.behaviours = behaviours
    
    on_apply = _composite_method("on_apply")
    on_tick = _composite_method("on_tick")
    on_remove = _composite_method("on_remove")

    on_attack = _composite_method("on_attack")
    on_cast = _composite_method("on_cast")
    on_cast_end = _composite_method("on_cast_end")