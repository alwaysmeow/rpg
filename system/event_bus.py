from queue import Queue
from typing import Callable, Dict, List

from utils import load_config

class EventBus:
    def __init__(self, world, game_config_path):
        self.world = world
        self._queue: Queue = Queue()
        self._listeners: Dict[type, List[Callable]] = {}

        config = load_config(game_config_path)
        self.emits_per_tick_limit = config["emits_per_tick_limit"]

    def queue(self, event):
        print(event)
        self._queue.put(event)
        return event

    def process(self):
        iterations = 0
        while self._queue and iterations < self.emits_per_tick_limit:
            event = self._queue.get()
            self.emit(event)
            iterations += 1
    
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