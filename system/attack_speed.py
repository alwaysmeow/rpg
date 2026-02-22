from component.stats import AttackSpeed, AttackDelay
from component.tag import Attack
from component.ability import Owner, Cooldown

from shared.formula import AttackDelayFormula
from shared.event_type import EventType
from shared.event_result import StatUpdateResult
from shared.statref import StatRef

class AttackSpeedSystem:
    def __init__(self, world):
        self.world = world

        self.world.events.subscribe(EventType.STAT_UPDATE, self._on_stat_update)
    
    def create_attack_speed(self, entity_id, value):
        # TODO: maybe move to event handler
        self.world.stats_system.create_stat(entity_id, AttackSpeed(value))
        self.world.stats_system.create_stat(entity_id, AttackDelay(0, AttackDelayFormula))

        self.world.events.schedule(
            self.world.time.now,
            lambda: StatUpdateResult(
                entity_id,
                StatRef(AttackSpeed, "base_value"),
                value
            ),
            EventType.STAT_UPDATE,
        )
    
    def _search_attack_ability(self, entity_id):
        attacks = self.world.query_by_tag(Attack)
        for ability_id in attacks:
            owner = self.world.get_component(ability_id, Owner)
            if owner and owner.unit_id == entity_id:
                return ability_id

    def _on_stat_update(self, result: StatUpdateResult):
        component_type, value_name = result.statref
        if component_type == AttackDelay and value_name == "effective_value":
            new_cooldown_regen = 1 / result.new_value
            attack_ability_id = self._search_attack_ability(result.entity_id)

            cooldown = self.world.get_or_create_component(attack_ability_id, Cooldown)
            cooldown.base_regen = new_cooldown_regen
            cooldown.effective_regen = new_cooldown_regen
            print(new_cooldown_regen)