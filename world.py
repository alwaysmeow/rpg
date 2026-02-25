from typing import Type, Any, Set, Dict
from collections import defaultdict
from rich.console import Console

from system.time import TimeSystem
from system.event.event import EventSystem
from system.combat import CombatSystem
from system.damage import DamageSystem
from system.cooldown import CooldownSystem
from system.ability import AbilitySystem
from system.resource import ResourceSystem
from system.stats.stats import StatsSystem
from system.attack_speed import AttackSpeedSystem
from system.god import God

from ui.logger import Logger

class World:
    def __init__(self, game_config_path="config/game.json"):
        self.systems: Dict[Type, Any] = {}

        self.registry_system(TimeSystem())
        self.registry_system(EventSystem(self, game_config_path))
        self.registry_system(CombatSystem(self))
        self.registry_system(DamageSystem(self, game_config_path))
        self.registry_system(CooldownSystem(self, game_config_path))
        self.registry_system(AbilitySystem(self))
        self.registry_system(ResourceSystem(self))
        self.registry_system(StatsSystem(self))
        self.registry_system(AttackSpeedSystem(self))

        # Temporary object
        self.god = God(self)

        # TODO: move out
        console = Console()
        self.logger = Logger(self, console.print)

        self.entities: Set[int] = set()
        self.components: Dict[Type, Dict[int, Any]] = defaultdict(dict)
        self.tags: Dict[Type, Set[int]] = defaultdict(set)
        self._next_entity_id = 0

    def update(self, delta):
        now = self.get_system(TimeSystem).advance(delta)
        self.get_system(CooldownSystem).update(delta)
        self.get_system(ResourceSystem).update(delta)
        self.get_system(EventSystem).process(now)

    def create_entity(self) -> int:
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        self.entities.add(entity_id)
        return entity_id
    
    def registry_system(self, system):
        self.systems[type(system)] = system
        return system

    def get_system(self, system_type):
        return self.systems.get(system_type)

    def add_component(self, entity: int, component: Any):
        self.components[type(component)][entity] = component
    
    def has_component(self, entity: int, component_type: Type) -> bool:
        return entity in self.components[component_type]
    
    def get_component(self, entity: int, component_type: Type) -> Any:
        return self.components[component_type].get(entity)
    
    def get_or_create_component(self, entity: int, component_type: Type) -> Any:
        component = self.components[component_type].get(entity, None)
        if component is None:
            component = component_type()
            self.components[component_type][entity] = component
        return component
    
    def query_by_component( # TODO: rework filters structure
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

    def query_by_components( # TODO: rework filters structure
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