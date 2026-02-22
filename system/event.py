import heapq
from typing import Callable, Dict, List

from shared.event_type import EventType

from utils import load_config

class Event:
    def __init__(self, time, handler, event_type = None, unique_key = None, seq = 0):
        self.time = time
        self.handler = handler
        self.type = event_type
        self.unique_key = unique_key
        self.seq = seq

    def __lt__(self, other):
        if self.time == other.time:
            if self.type.priority == other.type.priority:
                return self.seq < other.seq
            return self.type.priority > other.type.priority
        return self.time < other.time

class EventSystem:
    def __init__(self, world, game_config_path):
        self.world = world
        self._queue = []
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._unique_keys = set()
        self._seq: Dict[float, int] = {}

        config = load_config(game_config_path)
        self.events_per_tick_limit = config["events_per_tick_limit"]


    def schedule(self, time, handler, event_type = None, unique_key = None):
        if unique_key and unique_key in self._unique_keys:
            return None

        # Can be float error
        seq = self._seq.get(time, 0)
        self._seq[time] = seq + 1
        event = Event(time, handler, event_type, unique_key, seq)

        heapq.heappush(self._queue, event)
        if unique_key:
            self._unique_keys.add(unique_key)
        return event

    def process(self, now):
        iterations = 0
        while self._queue and self._queue[0].time <= now and iterations < self.events_per_tick_limit:
            event: Event = heapq.heappop(self._queue)
            self._unique_keys.discard(event.unique_key)
            event_result = event.handler()
            if event.type:
                self.emit(event.type, event_result)
            iterations += 1

        # Delete sequence counters if all events processed
        if iterations < self.events_per_tick_limit:
            self._clear_seq_dict(now)
    
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
    
    def _clear_seq_dict(self, now):
        keys_to_delete = [t for t in self._seq if t <= now]
        for t in keys_to_delete:
            del self._seq[t]