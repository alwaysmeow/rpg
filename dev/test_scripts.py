from system.combat import CombatSystem

def test_script(world):
    flaneur = world.god.create_unit("flaneur")
    world.god.create_autoattack(flaneur, 50)

    meowmeow = world.god.create_unit("meowmeow")
    world.god.create_autoattack(meowmeow, 20)

    world.get_system(CombatSystem).create_combat([
        [flaneur],
        [meowmeow]
    ])