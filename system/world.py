from typing import Type, Any, Set, Dict
from collections import defaultdict

from system.time import TimeSystem
from system.event import EventSystem
from system.entity import EntitySystem
from system.combat import CombatSystem
from system.logger import Logger

class World:
    def __init__(self):
        self.time = TimeSystem()
        self.events = EventSystem()
        self.logger = Logger(self)
        self.entity_system = EntitySystem(self)
        self.combat_system = CombatSystem(self)

        self.components: Dict[Type, Dict[int, Any]] = defaultdict(dict)
        self.entities: Set[int] = set()
        self._next_entity_id = 0

    def update(self, delta):
        self.time.advance(delta)
        self.events.process(self.time.now)

    def create_entity(self) -> int:
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        self.entities.add(entity_id)
        return entity_id
    
    def add_component(self, entity: int, component_type: Type, *data):
        component = component_type(*data)
        self.components[component_type][entity] = component
    
    def has_component(self, entity: int, component_type: Type) -> bool:
        return entity in self.components[component_type]
    
    def get_component(self, entity: int, component_type: Type):
        return self.components[component_type].get(entity)