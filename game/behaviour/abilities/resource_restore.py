from typing import Dict

from game.core.command import CastEndCommand, ResourceRestoreCommand

from game.component.behaviour import Behaviour
from game.component.ability import Owner, CastTime

class ResourceRestoreBehaviour(Behaviour):
    def __init__(self, resource: Dict[type, int]):
        self.resource = resource

    def on_cast(self, world, ability_id):
        from game.system.ability import AbilitySystem
        ability_system = world.get_system(AbilitySystem)

        cast_time = 0
        cast_time_component = world.get_component(ability_id, CastTime)
        if cast_time_component:
            cast_time = cast_time_component.value

        ability_system.schedule(CastEndCommand(ability_id), cast_time)

    def on_cast_end(self, world, ability_id):
        from game.system.ability import AbilitySystem
        ability_system = world.get_system(AbilitySystem)

        caster = world.get_component(ability_id, Owner)
        if caster and not caster.unit_id is None:
            ability_system.schedule(ResourceRestoreCommand(caster.unit_id, self.resource))
            caster_id = caster.unit_id