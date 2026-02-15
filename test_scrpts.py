from component.target import Target
from component.stats import AttackDamage

def test_script(world):
    flaneur = world.entity_system.create_unit("flaneur")
    world.add_component(flaneur, AttackDamage(10))
    world.logger.log_unit(flaneur)

    print()

    meowmeow = world.entity_system.create_unit("meowmeow")
    world.logger.log_unit(meowmeow)

    print()

    flaneur_attack = world.entity_system.create_autoattack(flaneur)

    print()

    world.add_component(flaneur, Target(meowmeow))
    world.combat_system.cast(flaneur_attack)

    world.logger.log_unit(meowmeow)

    world.update(0)