from entity.damage import Damage
from entity.damage_type import PhysicalDamageType
from component.stats import AttackDamage

def attack_handler(world, attacker_id, target_id):
    damage = world.get_component(attacker_id, AttackDamage)
    if not damage:
        return False
    
    Damage(attacker_id, target_id, PhysicalDamageType(), damage.value)
    # Process Damage

    return True