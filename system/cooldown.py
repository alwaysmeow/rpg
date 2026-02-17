from component.ability import Cooldown, Autocast

class CooldownSystem:
    def __init__(self, world):
        self.world = world
    
    def _update_ability_cooldown(self, cooldown, delta):
        cooldown.value += cooldown.effective_regen * delta

    def update(self, delta):
        for ability_id in self.world.components[Cooldown]:
            cooldown = self.world.get_component(ability_id, Cooldown)
            self._update_ability_cooldown(cooldown, delta)

            autocast = self.world.components[Autocast][ability_id]
            if autocast and autocast.value and cooldown.value == 1:
                self.world.ability_system.cast(ability_id)