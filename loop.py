from rich.console import Console

from engine.game import GameLoop
from engine.clock import Clock

from game.world import GameWorld

from ui.logger import Logger
from ui.app import GameApp

from dev.test_scripts import *

class Loop(GameLoop):
    def __init__(self, engine_config_path="config/engine.json", game_config_path="config/game.json"):
        self.world = GameWorld(game_config_path)

        console = Console()
        self.logger = Logger(self.world, console.print)
        self.world.logger = self.logger

        self.ui_app = GameApp(self.logger)

        super().__init__(self.world, Clock(), engine_config_path)
    
    def run(self):
        self.ui_app.run()
        super().run()
    
    def test(self):
        test_script(self.world)