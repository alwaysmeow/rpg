from rich.console import Console

from engine.app import Application

from game.world import GameWorld

from ui.logger import Logger
from ui.renderer import Renderer

from dev.test_scripts import *

class GameApp(Application):
    def __init__(self, engine_config_path="config/engine.json", game_config_path="config/game.json"):
        super().__init__(GameWorld(game_config_path), Renderer(), engine_config_path)

        self.test()
        self.world.logger = Logger(self.world, Console().print)

    def run(self):
        super().run()

    def test(self):
        test_script(self.world)