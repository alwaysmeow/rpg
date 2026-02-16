from component.name import Name
from component.stats import Armor, MagicResist, Health
from component.ability import Cooldown

class Logger:
    def __init__(self, world):
        self.world = world
    
    def log_unit(self, unit_id):
        print(f"\nName: {self.world.components[Name][unit_id].name}")
        print(f"Health: {self.world.components[Health][unit_id].value} / {self.world.components[Health][unit_id].effective_max_value}")
        print(f"Armor: {self.world.components[Armor][unit_id].effective_value}")
        print(f"Magic Resist: {self.world.components[MagicResist][unit_id].effective_value}")
    
    def log_ability(self, ability_id):
        print(f"\nID: {ability_id}")
        print(f"Cooldown: {self.world.components[Cooldown][ability_id].value} / {self.world.components[Cooldown][ability_id].effective_max_value}")

    def error(self, text):
        print(f"\n- ERROR: {text} - {self.world.time.now}\n")

    def log(self, text):
        print(f"\n- LOG: {text} - {self.world.time.now}\n")