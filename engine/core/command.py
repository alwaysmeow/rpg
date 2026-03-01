from typing import TypeVar, Generic

from engine.core.event import BaseEvent

E = TypeVar("E", bound=BaseEvent)

class Command(Generic[E]):
    priority = 0

    def execute(self, world) -> E:
        raise NotImplementedError
    
    def unique_key(self):
        return None