from rich.console import Console
import json
from dataclasses import asdict

from engine.app import Application

from game.world import GameWorld

from ui.logger import Logger
from ui.hud_renderer import HUDRenderer

from dev.test_scripts import *

class GameApp(Application):
    def __init__(self, engine_config_path="config/engine.json", game_config_path="config/game.json"):
        renderer = HUDRenderer()
        super().__init__(GameWorld(game_config_path), renderer, engine_config_path)

        renderer.bridge = self.bridge

        self.test()
        console = Console()
        self.world.logger = Logger(self.world, sink=renderer.get_sink())

    def run(self):
        super().run()

    def test(self):
        test_script(self.world)