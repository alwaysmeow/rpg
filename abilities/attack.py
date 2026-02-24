from system.event.event import EventSystem
from system.time import TimeSystem

from core.damage_type import DamageType
from core.command import DamageCommand

from component.stats import AttackDamage

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