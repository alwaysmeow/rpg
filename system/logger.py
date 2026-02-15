from component.name import Name
from component.stats import Armor, MagicResist, Health

class Logger:
    def __init__(self, world):
        self.world = world
    
    def log_unit(self, unit_id):
        print(f"Name: {self.world.components[Name][unit_id].name}")
        print(f"Health: {self.world.components[Health][unit_id].value} / {self.world.components[Health][unit_id].effective_max_value}")
        print(f"Armor: {self.world.components[Armor][unit_id].effective_value}")
        print(f"Magic Resist: {self.world.components[MagicResist][unit_id].effective_value}")
    
    def error(self, text):
        print(f"\n- ERROR: {text}\n\n")