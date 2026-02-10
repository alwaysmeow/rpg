from system.world import World
from system.clock import Clock
from game import GameLoop

from system.damage_pipeline import *

world = World()
clock = Clock()
loop = GameLoop(world, clock)

loop.run()
