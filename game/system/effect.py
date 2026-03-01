from engine.system.system import System

from game.component.effect import EffectDuration, CompositeBehaviour
from game.core.event import EffectApplyEvent, EffectTickEvent, EffectRemoveEvent

class EffectSystem(System):
    def create_effect(self):
        pass

    def apply(self, effect_id):
        self._invoke(effect_id, "on_apply")
        return EffectApplyEvent(effect_id)

    def tick(self, effect_id):
        self._invoke(effect_id, "on_tick")
        return EffectTickEvent(effect_id)

    def remove(self, effect_id):
        self._invoke(effect_id, "on_remove")
        return EffectRemoveEvent(effect_id)
    
    def _invoke(self, effect_id, method_name):
        behaviour = self.world.get_component(effect_id, CompositeBehaviour)
        if behaviour:
            getattr(behaviour, method_name)(effect_id)

    def effect_still_active(self, effect_id):
        duration_component = self.world.get_component(effect_id, EffectDuration)
        return duration_component and duration_component.remaining > 0
    
    def effect_still_active(self, effect_id):
        duration_component = self.world.get_component(effect_id, EffectDuration)
        return duration_component and duration_component.remaining > 0