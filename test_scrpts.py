def test_script(world):
    flaneur = world.entity_system.create_unit("flaneur")
    world.logger.log_unit(flaneur)

    meowmeow = world.entity_system.create_unit("meowmeow")
    world.logger.log_unit(meowmeow)

    world.entity_system.create_autoattack(flaneur)
    world.entity_system.create_autoattack(meowmeow)

    world.combat_system.create_combat([
        [flaneur],
        [meowmeow]
    ])