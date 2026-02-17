from component.name import Name
from component.stats import Armor, MagicResist, Health
from component.ability import Cooldown

class Logger:
    def __init__(self, world):
        self.world = world
    
    def log_unit(self, unit_id):
        print(f"\nName: {self.world.get_component(unit_id, Name).name}")
        print(f"Health: {self.world.get_component(unit_id, Health).value} / {self.world.get_component(unit_id, Health).effective_max_value}")
        print(f"Armor: {self.world.get_component(unit_id, Armor).effective_value}")
        print(f"Magic Resist: {self.world.get_component(unit_id, MagicResist).effective_value}")
    
    def log_ability(self, ability_id):
        print(f"\nID: {ability_id}")
        print(f"Cooldown: {self.world.get_component(ability_id, Cooldown).value} / {self.world.get_component(ability_id, Cooldown).effective_max_value}")

    def error(self, text):
        print(f"\n- ERROR: {text} - {self.world.time.now}\n")

    def log(self, text):
        print(f"\n- LOG: {text} - {self.world.time.now}\n")