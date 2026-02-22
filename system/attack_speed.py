from component.stats import AttackSpeed, AttackDelay
from component.tag import Attack
from component.ability import Owner, Cooldown

from shared.formula import AttackDelayFormula
from shared.event_type import EventType
from shared.event_result import StatsUpdateResult
from shared.statref import StatRef

class AttackSpeedSystem:
    def __init__(self, world):
        self.world = world

        self.world.events.subscribe(EventType.STATS_UPDATE, self._on_stat_update)

    def create_attack_speed(self, entity_id, value): # TODO: move to stats system
        self.world.stats_system.create_stat(entity_id, AttackSpeed(value))
        self.world.stats_system.create_stat(entity_id, AttackDelay(0, AttackDelayFormula))

    def _search_attack_ability(self, entity_id):
        attacks = self.world.query_by_tag(Attack)
        for ability_id in attacks:
            owner = self.world.get_component(ability_id, Owner)
            if owner and owner.unit_id == entity_id:
                return ability_id

    def _on_stat_update(self, result: StatsUpdateResult):
        new_value = result.updated[StatRef(AttackDelay, "effective_value")]
        if new_value:
            attack_ability_id = self._search_attack_ability(result.entity_id)
            cooldown = self.world.get_or_create_component(attack_ability_id, Cooldown)

            cooldown.base_regen = cooldown.base_max_value / new_value
            cooldown.effective_regen = cooldown.effective_max_value / new_value