from system.event.scheduler import CommandScheduler
from system.event.bus import EventBus

class EventSystem:
    def __init__(self, world, game_config_path):
        self.bus = EventBus(world, game_config_path)
        self.scheduler = CommandScheduler(world, self.bus, game_config_path)

    def process(self, now):
        self.scheduler.start_process()

        # TODO: fix bus limit makes infinite cycle
        while self.scheduler.has_ready(now) or not self.bus.is_empty():
            self.scheduler.process_one(now)
            self.bus.process() 

        self.scheduler.end_process(now)