from engine.system.event.event import EventSystem
from engine.system.time import TimeSystem

from game.core.damage_type import DamageType
from game.core.command import DamageCommand

from game.component.stats import AttackDamage

def attack_handler(world, attacker_id, target_id):
    damage = world.get_component(attacker_id, AttackDamage)
    if not damage:
        return False

    # TODO: simplify
    world.get_system(EventSystem).scheduler.schedule(
        world.get_system(TimeSystem).now,
        DamageCommand(attacker_id, target_id, DamageType.Physical, damage.effective_value)
    )

    return True