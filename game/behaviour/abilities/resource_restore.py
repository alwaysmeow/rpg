from typing import Dict

from game.core.command import ResourceRestoreCommand

from game.component.behaviour import Behaviour
from game.component.ability import Owner

class ResourceRestoreBehaviour(Behaviour):
    def __init__(self, resource: Dict[type, int]):
        self.resource = resource

    def _schedule_restore(self, world, ability_id):
        caster = world.get_component(ability_id, Owner)
        if caster and not caster.unit_id is None:
            world.schedule(ResourceRestoreCommand(caster.unit_id, self.resource))

    def on_cast_end(self, world, ability_id):
        self._schedule_restore(world, ability_id)

    def on_attack(self, world, ability_id):
        self._schedule_restore(world, ability_id)