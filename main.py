from world import World
from clock import Clock
from game import GameLoop

from dev.test_scripts import *

game_config_path="config/game.json"
world = World(game_config_path)

test_script(world)

clock = Clock()
loop = GameLoop(world, clock)

loop.run()
