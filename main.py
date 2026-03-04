from engine.clock import Clock
from engine.game import GameLoop

from game.world import GameWorld

from ui.app import GameApp

from dev.test_scripts import *

# game_config_path="config/game.json"
# world = GameWorld(game_config_path)

# test_script(world)

# clock = Clock()
# loop = GameLoop(world, clock)

# loop.run()

GameApp().run()