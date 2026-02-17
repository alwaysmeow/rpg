from component.ability import Cooldown, Autocast

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
                self.world.ability_system.autocast_trigger(ability_id)