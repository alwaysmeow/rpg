from component.ability import Cooldown, Owner
from component.tag import Attack
from component.stats import AttackDelay

from shared.command import *
from shared.event import CooldownUnsetEvent, CooldownSetEvent, CastEndEvent, AttackEvent

from utils import load_config

class CooldownSystem:
    def __init__(self, world, game_config_path="config/game.json"):
        self.world = world

        config = load_config(game_config_path)
        self.attack_speed_coefficient = config["attack_speed_coefficient"]
    
    def cooldown_set(self, ability_id):
        cooldown = self.world.get_component(ability_id, Cooldown)
        if cooldown:
            cooldown.value = 0
        return CooldownSetEvent(ability_id)

    def cooldown_unset(self, ability_id):
        return CooldownUnsetEvent(ability_id)

    def _update_ability_cooldown(self, cooldown, delta):
        old_value = cooldown.value
        cooldown.value += cooldown.effective_regen * delta
        return cooldown.value - old_value

    def update(self, delta):
        for ability_id in self.world.components[Cooldown]:
            cooldown = self.world.get_component(ability_id, Cooldown)

            progress = 0
            progress = self._update_ability_cooldown(cooldown, delta)

            if progress and progress > 0 and cooldown.value >= 1:
                self.world.events.scheduler.schedule(
                    self.world.time.now,
                    CooldownUnsetCommand(ability_id)
                )