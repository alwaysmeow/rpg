from system.event.scheduler import CommandScheduler
from system.event.bus import EventBus

class EventSystem:
    def __init__(self, world, game_config_path):
        self.scheduler = CommandScheduler(world, game_config_path)
        self.bus = EventBus(world, game_config_path)

    def process(self, now):
        self.scheduler.process(now)
        self.bus.process()