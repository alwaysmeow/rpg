from system.time import TimeSystem
from event_queue import EventQueue

class World:
    def __init__(self):
        self.time = TimeSystem()
        self.events = EventQueue()

    def update(self, delta):
        self.time.advance(delta)
        self.events.process(self.time.now)