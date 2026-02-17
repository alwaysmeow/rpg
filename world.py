from typing import Type, Any, Set, Dict
from collections import defaultdict

from system.time import TimeSystem
from system.event import EventSystem
from system.entity import EntityFactory
from system.combat import CombatSystem
from system.logger import Logger
from system.damage import DamageSystem
from system.cooldown import CooldownSystem
from system.ability import AbilitySystem
from system.regeneration import RegenerationSystem

from component.tag import Tag

class World:
    def __init__(self):
        self.time = TimeSystem()
        self.events = EventSystem(self)
        self.logger = Logger(self)
        self.entity_factory = EntityFactory(self)
        self.combat_system = CombatSystem(self)
        self.damage_system = DamageSystem(self)
        self.cooldown_system = CooldownSystem(self)
        self.ability_system = AbilitySystem(self)
        self.regeneration_system = RegenerationSystem(self)

        self.entities: Set[int] = set()
        self.components: Dict[Type, Dict[int, Any]] = defaultdict(dict)
        self.tags: Dict[Type, Set[int]] = defaultdict(set)
        self._next_entity_id = 0

    def update(self, delta):
        self.time.advance(delta)
        self.cooldown_system.update(delta)
        self.regeneration_system.update(delta)
        self.events.process(self.time.now)

    def create_entity(self) -> int:
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        self.entities.add(entity_id)
        return entity_id
    
    def add_component(self, entity: int, component: Any):
        self.components[type(component)][entity] = component
    
    def has_component(self, entity: int, component_type: Type) -> bool:
        return entity in self.components[component_type]
    
    def get_component(self, entity: int, component_type: Type) -> Any:
        return self.components[component_type].get(entity)
    
    def query_by_component(
        self, 
        component_type: Type, 
        include_filters: Dict[str, Any] | None = None, 
        exclude_filters: Dict[str, Any] | None = None
    ) -> Set[int]:
        result = set()

        for entity_id, component in self.components[component_type].items():
            match = True

            if not include_filters is None:
                for attr, expected_values in include_filters.items():
                    if not hasattr(component, attr) or not getattr(component, attr) in expected_values:
                        match = False
                        break
            
            if not exclude_filters is None:
                for attr, unexpected_values in exclude_filters.items():
                    if hasattr(component, attr) and getattr(component, attr) in unexpected_values:
                        match = False
                        break

            if match:
                result.add(entity_id)

        return result

    def query_by_components(
        self,
        filters: Dict[Type, Any] | None = None,
    ) -> Set[int]:
        if not filters:
            return self.entities.copy()

        component_types = list(filters.keys())
        first_type = component_types[0]

        result = self.query_by_component(
            first_type,
            include_filters=filters[first_type].get("include"),
            exclude_filters=filters[first_type].get("exclude")
        )

        for component_type in component_types[1:]:
            result &= self.query_by_component(
                component_type,
                include_filters=filters[component_type].get("include"),
                exclude_filters=filters[component_type].get("exclude")
            )

        return result

    def add_tag(self, entity: int, tag: Type):
        self.tags[tag].add(entity)
    
    def remove_tag(self, entity: int, tag: Type):
        self.tags[tag].discard(entity)
    
    def has_tag(self, entity: int, tag: Type) -> bool:
        return entity in self.tags[tag]
    
    def get_tags(self, entity: int) -> Set[Type]:
        return {tag_type for tag_type, entities in self.tags.items() if entity in entities}
    
    def query_by_tag(self, tag: Type) -> Set[int]:
        return self.tags[tag].copy()