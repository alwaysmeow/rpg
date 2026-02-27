from system.combat import CombatSystem

def test_script(world):
    flaneur = world.unit_builder.build_from_file("templates/units/flaneur.json")
    world.god.create_autoattack(flaneur, 50)

    meowmeow = world.unit_builder.build_from_file("templates/units/meowmeow.json")
    world.god.create_autoattack(meowmeow, 20)

    world.get_system(CombatSystem).create_combat([
        [flaneur],
        [meowmeow]
    ])