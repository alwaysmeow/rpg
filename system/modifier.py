from shared.modifier_type import ModifierType

from component.modifier import ModifierData, TargetModifiers
from component.tag import Modifier

class ModifierSystem:
    def __init__(self, world):
        self.world = world
    
        self.stat_base_value_names_map = {
            "effective_value": "base_value",
            "effective_max_value": "base_max_value",
            "effective_regen": "base_regen"
        }

    def create_modifier(self, stat: type, value: float, type: ModifierType):
        modifier_id = self.world.create_entity()

        self.world.add_component(modifier_id, ModifierData(stat, value, type))
        self.world.add_tag(modifier_id, Modifier)

        return modifier_id

    def _apply_modifiers(self, base_value, modifiers: ModifierData):
        flat = 0
        multiplier = 0
        for modifier in modifiers:
            match modifier.type:
                case ModifierType.Flat:
                    flat += modifier.value
                case ModifierType.Multiplier:
                    multiplier += modifier.value
        return (base_value + flat) * (1 + multiplier)
    
    def _update_effective_value(self, entity_id, statref):
        component_type, value_name = statref
        component = self.world.get_component(entity_id, component_type)

        if component is None:
            self.world.logger.error(f"Component {component_type.__name__} should exist")
            return
        
        if not value_name in self.stat_base_value_names_map:
            self.world.logger.error(f"_update_effective_value method updates only effective values")
            return

        modifiers = []
        modifiers_component = self.world.get_component(entity_id, TargetModifiers)

        if modifiers_component:
            modifiers_ids = modifiers_component.map[component_type]
            for modifier_id in modifiers_ids:
                modifier_data = self.world.get_component(modifier_id, ModifierData)
                if modifier_data:
                    modifiers.append(modifier_data)

        base_value_name = self.stat_base_value_names_map[value_name]
        base_value = getattr(component, base_value_name)
        new_effective_value = self._apply_modifiers(base_value, modifiers)

        setattr(component, value_name, new_effective_value)

        return new_effective_value