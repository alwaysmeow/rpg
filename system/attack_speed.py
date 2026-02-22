from component.stats import AttackSpeed, AttackDelay
from component.tag import Attack
from component.ability import Owner, Cooldown

from shared.formula import AttackDelayFormula
from shared.event_type import EventType
from shared.event_result import StatsCreateResult, StatsUpdateResult
from shared.statref import StatRef

class AttackSpeedSystem:
    def __init__(self, world):
        self.world = world

        self.world.events.subscribe(EventType.STATS_CREATE, self._on_stats_create)
        self.world.events.subscribe(EventType.STATS_UPDATE, self._on_stats_update)

    def _search_attack_ability(self, entity_id):
        attacks = self.world.query_by_tag(Attack)
        for ability_id in attacks:
            owner = self.world.get_component(ability_id, Owner)
            if owner and owner.unit_id == entity_id:
                return ability_id

    def _update_attack_ability_cooldown(self, entity_id, attack_delay_value):
        attack_ability_id = self._search_attack_ability(entity_id)
        cooldown = self.world.get_or_create_component(attack_ability_id, Cooldown)

        cooldown.base_regen = cooldown.base_max_value / attack_delay_value
        cooldown.effective_regen = cooldown.effective_max_value / attack_delay_value

    def _on_stats_create(self, result: StatsCreateResult):
        for component in result.created:
            if type(component) == AttackDelay:
                new_value = component.effective_value
                return self._update_attack_ability_cooldown(result.entity_id, new_value)

    def _on_stats_update(self, result: StatsUpdateResult):
        new_value = result.updated[StatRef(AttackDelay, "effective_value")]
        if new_value:
            return self._update_attack_ability_cooldown(result.entity_id, new_value)