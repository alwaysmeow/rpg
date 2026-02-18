import heapq
from typing import Callable, Dict, List
from dataclasses import dataclass

from entity.event_type import EventType
from entity.damage_type import DamageType

@dataclass
class AttackEventResult:
    attacker_id: int
    target_id: int

@dataclass
class CastEventResult:
    caster_id: int
    target_id: int
    ability_id: int

@dataclass
class CooldownEventResult:
    ability_id: int

@dataclass
class CombatEventResult:
    combat_id: int
    teams: list[list[int]]

@dataclass
class DamageEventResult:
    source_id: int
    target_id: int
    amount: int
    damage_type: DamageType

@dataclass
class DeathEventResult:
    victim_id: int
    killer_id: int

class Event:
    def __init__(self, time, handler, event_type = None, unique_key = None):
        self.time = time
        self.handler = handler
        self.type = event_type
        self.unique_key = unique_key

    def __lt__(self, other):
        if self.time == other.time:
            return self.type.priority > other.type.priority
        return self.time < other.time

class EventSystem:
    def __init__(self, world):
        self.world = world
        self._queue = []
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._unique_keys = set()

    def schedule(self, time, handler, event_type = None, unique_key = None):
        if unique_key and unique_key in self._unique_keys:
            self.world.logger.error(f"Can't schedule duplicate of {unique_key}")
            return None
        event = Event(time, handler, event_type, unique_key)
        heapq.heappush(self._queue, event)
        if unique_key:
            self._unique_keys.add(unique_key)
        return event

    def process(self, now):
        # TODO: max iterations
        while self._queue and self._queue[0].time <= now:
            event = heapq.heappop(self._queue)
            event_result = event.handler()
            self.world.logger.log(f"Event occured: {event.type} with result = {event_result}")
            if event.type:
                self.emit(event.type, event_result)
    
    def subscribe(self, event_type, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type, callback):
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)
    
    def emit(self, event_type: EventType, event_result):
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(event_result)