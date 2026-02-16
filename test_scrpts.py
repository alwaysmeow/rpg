from component.target import Target

def test_script(world):
    flaneur = world.entity_system.create_unit("flaneur")
    world.logger.log_unit(flaneur)

    meowmeow = world.entity_system.create_unit("meowmeow")
    world.logger.log_unit(meowmeow)

    flaneur_attack = world.entity_system.create_autoattack(flaneur)

    world.add_component(flaneur, Target(meowmeow))
    world.combat_system.cast(flaneur_attack)

    world.update(0)

    world.logger.log_unit(meowmeow)

def test_script2(world):
    flaneur = world.entity_system.create_unit("flaneur")
    world.entity_system.create_autoattack(flaneur)
    world.logger.log_unit(flaneur)

    meowmeow = world.entity_system.create_unit("meowmeow")
    world.add_component(flaneur, Target(meowmeow))

    world.update(0)