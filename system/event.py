import heapq
from enum import Enum
from typing import Callable, Dict, List

class EventType(Enum):
    ATTACK = "on_attack"
    CAST_START = "on_cast_start"
    CAST_END = "on_cast_end"
    COOLDOWN_END = "on_cooldown_end"
    DAMAGE = "on_damage"
    DEATH = "on_death"

class Event:
    def __init__(self, time, handler, event_type = None, data = None):
        self.time = time
        self.handler = handler
        self.type = event_type
        self.data = data if data is not None else {}

    def __lt__(self, other):
        return self.time < other.time

class EventSystem:
    def __init__(self):
        self._queue = []
        self._listeners: Dict[EventType, List[Callable]] = {}

    def schedule(self, time, handler, event_type = None, data = None):
        heapq.heappush(self._queue, Event(time, handler, event_type, data))

    def process(self, now):
        while self._queue and self._queue[0].time <= now:
            event = heapq.heappop(self._queue)
            event.handler()
            if event.type:
                self.emit(event.type, event.data)
    
    def subscribe(self, event_type, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type, callback):
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)
    
    def emit(self, event_type: EventType, data: dict = None):
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(data or {})