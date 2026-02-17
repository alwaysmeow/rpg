def test_script(world):
    flaneur = world.entity_factory.create_unit("flaneur")
    world.entity_factory.create_autoattack(flaneur)

    meowmeow = world.entity_factory.create_unit("meowmeow")
    world.entity_factory.create_autoattack(meowmeow)

    world.combat_system.create_combat([
        [flaneur],
        [meowmeow]
    ])