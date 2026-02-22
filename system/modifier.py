from shared.modifier_type import ModifierType
from shared.event_type import EventType
from shared.event_result import StatUpdateResult

from component.modifier import ModifierData, SourceModifiers, TargetModifiers
from component.tag import Modifier

class ModifierSystem:
    def __init__(self, world):
        self.world = world

        self.world.events.subscribe(EventType.STAT_UPDATE, self._on_stat_update)
    
    def create_modifier(self, stat: type, value: float, type: ModifierType):
        modifier_id = self.world.create_entity()

        self.world.add_component(modifier_id, ModifierData(stat, value, type))
        self.world.add_tag(modifier_id, Modifier)

        return modifier_id
    
    # Legacy
    def apply_modifiers(self, base_value, modifiers):
        flat = 0
        multiplier = 0
        for modifier in modifiers:
            match modifier.type:
                case ModifierType.Flat:
                    flat += modifier.value
                case ModifierType.Multiplier:
                    multiplier += modifier.value
        return (base_value + flat) * (1 + multiplier)
    
    def _on_stat_update(self, result: StatUpdateResult):
        base_values = ["base_value", "base_max_value", "base_regen"]

        if result.statref.value_name in base_values:
            # TODO apply modifiers and STAT_UPDATE event
            pass