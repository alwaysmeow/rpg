from shared.modifier_type import ModifierType
from shared.event_type import EventType
from shared.event_result import StatUpdateResult
from shared.statref import StatRef

from component.modifier import ModifierData, SourceModifiers, TargetModifiers
from component.tag import Modifier

class ModifierSystem:
    def __init__(self, world):
        self.world = world

        self.world.events.subscribe(EventType.STAT_UPDATE, self._on_stat_update)

        self.stat_value_names_map = {
            "base_value": "effective_value",
            "base_max_value": "effective_max_value",
            "base_regen": "effective_regen"
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
    
    def _on_stat_update(self, result: StatUpdateResult):
        component_type, value_name = result.statref

        # TODO: check depth

        # Update effective value if base value updated
        if value_name in self.stat_value_names_map:
            modifiers = []
            modifiers_component = self.world.get_component(result.entity_id, TargetModifiers)

            if modifiers_component:
                modifiers_ids = modifiers_component.map[component_type]
                for modifier_id in modifiers_ids:
                    modifier_data = self.world.get_component(modifier_id, ModifierData)
                    if modifier_data:
                        modifiers.append(modifier_data)
            
            effective_value_name = self.stat_value_names_map[value_name]
            new_effective_value = self._apply_modifiers(result.new_value, modifiers)
            
            # TODO: maybe need unique key
            # What if we create two similar events in one tick?
            self.world.events.schedule(
                self.world.time.now,
                self._create_stat_update_event_handler(
                    result.entity_id, 
                    StatRef(component_type, effective_value_name),
                    new_effective_value,
                    result.depth + 1
                ),
                EventType.STAT_UPDATE
            )

    def _create_stat_update_event_handler(self, entity_id, statref, new_value, depth):
        component_type, value_name = statref
        component = self.world.get_component(entity_id, component_type)

        if component is None:
            self.world.logger.error(f"Component {component_type.__name__} should exist")
            return lambda: StatUpdateResult(None, None, None)

        def handler():
            setattr(component, value_name, new_value)
            return StatUpdateResult(entity_id, StatRef(component_type, value_name), new_value, depth)

        return handler