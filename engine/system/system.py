from engine.system.event.event import EventSystem
from engine.system.time import TimeSystem

from engine.core.command import Command

class System:
    def __init__(self, world):
        self.world = world
    
    def schedule(self, command: Command, delay: float = 0):
        self.world.schedule(command, delay)

    def schedule_at(self, command: Command, time: float = None):
        self.world.schedule_at(command, time)

    def cancel_unique_command(self, unique_key):
        self.world.cancel_unique_command(unique_key)
    
    def subscribe(self, event_type: type, method):
        self.world.get_system(EventSystem).bus.subscribe(event_type, method)