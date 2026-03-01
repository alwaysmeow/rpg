from queue import Queue
from typing import Callable, Dict, List

class EventBus:
    def __init__(self, world, game_config_path):
        self.world = world
        self._queue: Queue = Queue()
        self._listeners: Dict[type, List[Callable]] = {}

    def queue(self, event):
        self._queue.put(event)
        return event

    def process_one(self):
        if self.has_pending():
            event = self._queue.get()
            self.emit(event)
    
    def subscribe(self, event_type, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type, callback):
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)
    
    def emit(self, event):
        if type(event) in self._listeners:
            for callback in self._listeners[type(event)]:
                callback(event)
    
    def has_pending(self):
        return not self._queue.empty()