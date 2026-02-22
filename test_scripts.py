def test_script(world):
    flaneur = world.entity_factory.create_unit("flaneur")
    world.entity_factory.create_autoattack(flaneur, 50)

    meowmeow = world.entity_factory.create_unit("meowmeow")
    world.entity_factory.create_autoattack(meowmeow, 50)

    world.combat_system.create_combat([
        [flaneur],
        [meowmeow]
    ])