from component.ability import Cooldown, Owner
from component.tag import Attack
from component.stats import AttackSpeed
from system.event import CooldownEventResult
from entity.event_type import EventType

from config_loader import load_config

class CooldownSystem:
    def __init__(self, world, game_config_path="config/game.json"):
        self.world = world

        config = load_config(game_config_path)
        self.attack_speed_coefficient = config["attack_speed_coefficient"]
    
    def _update_ability_cooldown(self, cooldown, delta):
        old_value = cooldown.value
        cooldown.value += cooldown.effective_regen * delta
        return cooldown.value - old_value

    def _update_attack_cooldown(self, cooldown, attack_speed, delta):
        old_value = cooldown.value
        cooldown_regen = attack_speed * self.attack_speed_coefficient # TODO: analize formula
        cooldown.value += cooldown_regen * delta
        return cooldown.value - old_value

    def update(self, delta):
        for ability_id in self.world.components[Cooldown]:
            cooldown = self.world.get_component(ability_id, Cooldown)

            if self.world.has_tag(ability_id, Attack):
                owner_id = self.world.get_component(ability_id, Owner)
                if owner_id:
                    attack_speed = self.world.get_component(owner_id.unit_id, AttackSpeed)
                    if attack_speed:
                        progress = self._update_attack_cooldown(cooldown, attack_speed.effective_value, delta)
            else:
                progress = self._update_ability_cooldown(cooldown, delta)

            if progress and progress > 0 and cooldown.value >= 1:
                self.world.events.schedule(
                    self.world.time.now,
                    self._create_cooldown_end_handler(ability_id),
                    EventType.COOLDOWN_END
                )
    
    def _create_cooldown_end_handler(self, ability_id):
        def cooldown_end_handler():
            return CooldownEventResult(ability_id)
        return cooldown_end_handler