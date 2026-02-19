from shared.damage_type import DamageType
from component.stats import AttackDamage

def attack_handler(world, attacker_id, target_id):
    damage = world.get_component(attacker_id, AttackDamage)
    if not damage:
        return False
    
    world.damage_system.queue_damage(attacker_id, target_id, DamageType.Physical, damage.effective_value)

    return True