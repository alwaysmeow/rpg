from component.ability import Cooldown
from system.event import CooldownEventResult
from entity.event_type import EventType

class CooldownSystem:
    def __init__(self, world):
        self.world = world
    
    def _update_ability_cooldown(self, cooldown, delta):
        old_value = cooldown.value
        cooldown.value += cooldown.effective_regen * delta
        return cooldown.value - old_value

    def update(self, delta):
        for ability_id in self.world.components[Cooldown]:
            cooldown = self.world.get_component(ability_id, Cooldown)
            progress = self._update_ability_cooldown(cooldown, delta)

            if progress > 0 and cooldown.value >= 1:
                self.world.events.schedule(
                    self.world.time.now,
                    self._create_cooldown_end_handler(ability_id),
                    EventType.COOLDOWN_END
                )
    
    def _create_cooldown_end_handler(self, ability_id):
        def cooldown_end_handler():
            return CooldownEventResult(ability_id)
        return cooldown_end_handler