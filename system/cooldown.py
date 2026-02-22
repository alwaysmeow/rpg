from component.ability import Cooldown, Owner
from component.tag import Attack
from component.stats import AttackDelay

from shared.event_type import EventType
from shared.event_result import CooldownEventResult, CastEventResult, AttackEventResult

from utils import load_config

class CooldownSystem:
    def __init__(self, world, game_config_path="config/game.json"):
        self.world = world

        config = load_config(game_config_path)
        self.attack_speed_coefficient = config["attack_speed_coefficient"]

        self.world.events.subscribe(EventType.ATTACK, self._on_cast)
        self.world.events.subscribe(EventType.CAST_END, self._on_cast)
    
    def _update_ability_cooldown(self, cooldown, delta):
        old_value = cooldown.value
        cooldown.value += cooldown.effective_regen * delta
        return cooldown.value - old_value

    def _update_attack_cooldown(self, cooldown, attack_delay, delta):
        # TODO: remove method
        old_value = cooldown.value
        if attack_delay:
            cooldown_regen = 1 / attack_delay
            cooldown.value += cooldown_regen * delta
        return cooldown.value - old_value

    def update(self, delta):
        for ability_id in self.world.components[Cooldown]:
            cooldown = self.world.get_component(ability_id, Cooldown)

            progress = 0
            if self.world.has_tag(ability_id, Attack):
                owner = self.world.get_component(ability_id, Owner)
                if owner:
                    attack_delay = self.world.get_component(owner.unit_id, AttackDelay)
                    if attack_delay:
                        progress = self._update_attack_cooldown(cooldown, attack_delay.effective_value, delta)
            else:
                progress = self._update_ability_cooldown(cooldown, delta)

            if progress and progress > 0 and cooldown.value >= 1:
                self.world.events.schedule(
                    self.world.time.now,
                    self._create_cooldown_unset_handler(ability_id),
                    EventType.COOLDOWN_UNSET
                )
    
    def _create_cooldown_unset_handler(self, ability_id):
        def cooldown_end_handler():
            return CooldownEventResult(ability_id)
        return cooldown_end_handler

    def _on_cast(self, result: AttackEventResult | CastEventResult):
        self._set_cooldown(
            self.world.get_component(result.ability_id, Cooldown)
        )
    
    def _set_cooldown(self, cooldown: Cooldown):
        if cooldown:
            cooldown.value = 0