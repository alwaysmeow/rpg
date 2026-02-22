from component.stats import AttackSpeed, AttackDelay

from shared.formula import AttackDelayFormula
from shared.event_type import EventType
from shared.event_result import StatUpdateResult
from shared.statref import StatRef

class AttackSpeedSystem:
    def __init__(self, world):
        self.world = world
    
    def create_attack_speed(self, entity_id, value):
        self.world.stats_system.create_stat(entity_id, AttackSpeed(value))
        self.world.stats_system.create_stat(entity_id, AttackDelay(0, AttackDelayFormula))

        self.world.events.schedule(
            self.time.now,
            lambda: StatUpdateResult(StatRef(AttackSpeed, "base_value")),
            EventType.STAT_UPDATE,
        )