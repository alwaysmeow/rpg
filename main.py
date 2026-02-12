from system.world import World
from system.clock import Clock
from game import GameLoop

from system.damage_pipeline import *

world = World()
world.unit_system.create_unit("flaneur")

print(world.entities)
print(world.components)

clock = Clock()
loop = GameLoop(world, clock)

loop.run()
