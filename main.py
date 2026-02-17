from world import World
from system.clock import Clock
from game import GameLoop

from test_scripts import *

world = World()
test_script(world)

clock = Clock()
loop = GameLoop(world, clock)

loop.run()
