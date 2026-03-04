from rich.console import Console

from engine.app import Application
from engine.clock import Clock

from game.world import GameWorld

from ui.logger import Logger
from ui.renderer import Renderer

from dev.test_scripts import *

class GameApp(Application):
    def __init__(self, engine_config_path="config/engine.json", game_config_path="config/game.json"):
        self.world = GameWorld(game_config_path)

        self.test()

        console = Console()
        self.logger = Logger(self.world, console.print)
        self.world.logger = self.logger

        super().__init__(self.world, Renderer(), engine_config_path)
    
    def run(self):
        super().run()
    
    def test(self):
        test_script(self.world)