from component.ability import Cooldown, Autocast

class CooldownSystem:
    def __init__(self, world):
        self.world = world
    
    def _update_ability_cooldown(self, cooldown, delta):
        cooldown.value += cooldown.effective_regen * delta

    def update(self, delta):
        for ability_id in self.world.components[Cooldown]:
            cooldown = self.world.components[Cooldown][ability_id]
            self._update_ability_cooldown(cooldown, delta)

            autocast = self.world.components[Autocast][ability_id]
            if autocast.value and cooldown.value == 1:
                self.world.logger.log(f"Ability {ability_id} autocasted")
                self.world.combat_system.cast(ability_id)