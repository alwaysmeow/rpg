import threading

from engine.bridge import Bridge
from engine.simulation import Simulation

class Application:
    def __init__(self, world, renderer, engine_config_path="config/engine.json"):
        self.bridge = Bridge()
        self.simulation = Simulation(world, self.bridge, engine_config_path)
        self.renderer = renderer

    def run(self):
        thread = threading.Thread(target=self.simulation.run, daemon=True)
        thread.start()
        self.renderer.run()
        self.simulation.stop()