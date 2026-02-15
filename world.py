from typing import Type, Any, Set, Dict
from collections import defaultdict

from system.time import TimeSystem
from system.event import EventSystem
from system.entity import EntitySystem
from system.combat import CombatSystem
from system.logger import Logger
from system.damage import DamageSystem

from component.tag import Tag

class World:
    def __init__(self):
        self.time = TimeSystem()
        self.events = EventSystem()
        self.logger = Logger(self)
        self.entity_system = EntitySystem(self)
        self.combat_system = CombatSystem(self)
        self.damage_system = DamageSystem(self)

        self.entities: Set[int] = set()
        self.components: Dict[Type, Dict[int, Any]] = defaultdict(dict)
        self.tags: Dict[Type, Set[int]] = defaultdict(set)
        self._next_entity_id = 0

    def update(self, delta):
        self.time.advance(delta)
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
    
    def add_tag(self, entity: int, tag: Type):
        self.tags[tag].add(entity)
    
    def remove_tag(self, entity: int, tag: Type):
        self.tags[tag].discard(entity)
    
    def has_tag(self, entity: int, tag: Type) -> bool:
        return entity in self.tags[tag]
    
    def get_tags(self, entity: int) -> Set[Type]:
        return {tag_type for tag_type, entities in self.tags.items() if entity in entities}