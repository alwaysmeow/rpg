from rich.console import Console
import json
from dataclasses import asdict

from engine.app import Application

from game.world import GameWorld

from ui.logger import Logger
from ui.renderer import Renderer

from dev.test_scripts import *

class GameApp(Application):
    def __init__(self, engine_config_path="config/engine.json", game_config_path="config/game.json"):
        renderer = Renderer()
        super().__init__(GameWorld(game_config_path), renderer, engine_config_path)

        self.test()
        self.world.logger = Logger(self.world, sink=renderer.get_sink(), markup=False)

    def run(self):
        super().run()

        # snapshot = self.world.build_snapshot()
        # print(json.dumps(asdict(snapshot), indent=4, sort_keys=True))

    def test(self):
        test_script(self.world)