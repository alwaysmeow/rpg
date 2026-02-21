from shared.modifier_type import ModifierType

from component.modifier import ModifierData, SourceModifiers, TargetModifiers
from component.tag import Modifier

class ModifierSystem:
    def __init__(self, world):
        self.world = world
    
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