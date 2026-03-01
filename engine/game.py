from utils import load_config

class GameLoop:
    def __init__(self, world, clock, engine_config_path = "config/engine.json"):
        self.world = world
        self.clock = clock

        config = load_config(engine_config_path)
        self.fixed_dt = 1 / config["updates_per_second"]
        self.max_steps = config["update_max_steps"]

        self.accumulator = 0.0
        self.time_scale = 1.0
        self.running = True

    def update(self):
        real_delta = self.clock.get_delta()
        self.accumulator += real_delta * self.time_scale

        steps = 0

        while self.accumulator >= self.fixed_dt and steps < self.max_steps:
            self.world.update(self.fixed_dt)
            self.accumulator -= self.fixed_dt
            steps += 1

    def render(self):
        pass

    def run(self):
        while self.running:
            self.update()
            self.render()
