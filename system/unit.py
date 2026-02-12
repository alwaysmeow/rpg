from component.stats import Armor, MagicResist, Health
from component.name import Name

class UnitSystem:
    def __init__(self, world):
        self.world = world

    def create_unit(self, name):
        unit_id = self.world.create_entity()

        self.world.add_component(unit_id, Name, name)
        self.world.add_component(unit_id, Health, 100, 0)
        self.world.add_component(unit_id, Armor)
        self.world.add_component(unit_id, MagicResist)

        return unit_id