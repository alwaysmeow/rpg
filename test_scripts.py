def test_script(world):
    flaneur = world.god.create_unit("flaneur")
    world.god.create_autoattack(flaneur, 50)

    meowmeow = world.god.create_unit("meowmeow")
    world.god.create_autoattack(meowmeow, 50)

    world.combat_system.create_combat([
        [flaneur],
        [meowmeow]
    ])