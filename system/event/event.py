from system.event.scheduler import CommandScheduler
from system.event.bus import EventBus

from utils import load_config

class EventSystem:
    def __init__(self, world, game_config_path):
        self.bus = EventBus(world, game_config_path)
        self.scheduler = CommandScheduler(world, self.bus, game_config_path)

        config = load_config(game_config_path)
        self.iterations_limit = config["commands_per_tick_limit"]

    def process(self, now):
        iterations = 0

        while not self.pipeline_is_empty(now) and iterations < self.iterations_limit:
            self.scheduler.process_one(now)
            self.bus.process_one()

            iterations += 1

        if iterations < self.iterations_limit:
            self.scheduler.clear_seq_dict(now)
    
    def pipeline_is_empty(self, now):
        return not self.scheduler.has_ready(now) and not self.bus.has_pending()