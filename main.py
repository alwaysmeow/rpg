from system.world import World
from system.clock import Clock
from game import GameLoop

world = World()

unit_id = world.unit_system.create_unit("flaneur")
world.logger.log_unit(unit_id)

clock = Clock()
loop = GameLoop(world, clock)

loop.run()
