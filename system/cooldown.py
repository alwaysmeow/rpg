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
            self._update_ability_cooldown(cooldown, delta)

            if cooldown.value >= 1:
                self._autocast_trigger(ability_id)
    
    def _autocast_trigger(self, ability_id):
        autocast = self.world.components[Autocast][ability_id]
        if autocast and autocast.value:
            self.world.ability_system.cast(ability_id)