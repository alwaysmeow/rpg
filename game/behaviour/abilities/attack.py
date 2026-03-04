from game.core.damage_type import DamageType
from game.core.command import DamageCommand

from game.component.stats import AttackDamage
from game.component.behaviour import Behaviour
from game.component.ability import Owner
from game.component.target import Target

class AttackBehaviour(Behaviour):
    def on_attack(self, world, ability_id):
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

        world.schedule(DamageCommand(attacker_id, target_id, DamageType.Physical, damage))