import time

from utils import load_config

from engine.clock import Clock
from engine.bridge import Bridge

class Simulation:
    def __init__(self, world, bridge: Bridge, engine_config_path = "config/engine.json"):
        self.world = world
        self.bridge = bridge
        self.clock = Clock()

        config = load_config(engine_config_path)
        self.fixed_dt = 1 / config["updates_per_second"]
        self.max_steps = config["update_max_steps"]

        self.accumulator = 0.0
        self.time_scale = 1.0
        self._running = True

    def update(self):
        real_delta = self.clock.get_delta()
        self.accumulator += real_delta * self.time_scale

        steps = 0
        while self.accumulator >= self.fixed_dt and steps < self.max_steps:
            self.world.update(self.fixed_dt)
            self.accumulator -= self.fixed_dt
            steps += 1

        if steps > 0:
            snapshot = self.world.build_snapshot()
            self.bridge.push_snapshot(snapshot)

        sleep_time = self.fixed_dt - self.accumulator
        if sleep_time > 0.001:
            time.sleep(sleep_time)

    def run(self):
        self._running = True
        while self._running:
            self.update()

    def stop(self):
        self._running = False
