from game.core.damage_type import DamageType
from game.core.command import DamageCommand, AttackCommand

from game.component.stats import AttackDamage
from game.component.behaviour import Behaviour
from game.component.ability import Owner, CastTime
from game.component.target import Target

class AttackBehaviour(Behaviour):
    def on_cast(self, world, ability_id):
        from game.system.ability import AbilitySystem
        ability_system = world.get_system(AbilitySystem)

        cast_time = 0
        cast_time_component = world.get_component(ability_id, CastTime)
        if cast_time_component:
            cast_time = cast_time_component.value

        ability_system.schedule(AttackCommand(ability_id), cast_time)

    def on_attack(self, world, ability_id):
        from game.system.ability import AbilitySystem
        ability_system = world.get_system(AbilitySystem)
        
        attacker_id, target_id = None, None
        damage = 0

        attacker = world.get_component(ability_id, Owner)

        if attacker and not attacker.unit_id is None:
            attacker_id = attacker.unit_id
        
            target_component = world.get_component(attacker_id, Target)
            if target_component:
                target_id = target_component.unit_id

            damage_component = world.get_component(attacker_id, AttackDamage)
            if damage_component:
                damage = damage_component.effective_value

        ability_system.schedule(DamageCommand(attacker_id, target_id, DamageType.Physical, damage))