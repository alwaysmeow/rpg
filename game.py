class GameLoop:
    def __init__(self, world, clock, fixed_dt=1/60):
        self.world = world
        self.clock = clock
        self.fixed_dt = fixed_dt

        self.accumulator = 0.0
        self.time_scale = 1.0
        self.running = True

    def update(self):
        real_delta = self.clock.get_delta()
        self.accumulator += real_delta * self.time_scale

        steps = 0
        MAX_STEPS = 5

        while self.accumulator >= self.fixed_dt and steps < MAX_STEPS:
            self.world.update(self.fixed_dt)
            self.accumulator -= self.fixed_dt
            steps += 1

    def render(self):
        pass

    def run(self):
        while self.running:
            self.update()
            self.render()
