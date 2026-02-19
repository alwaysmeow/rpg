from component.stats import Armor, MagicResist
from shared.formula import BaseArmorFormula, BaseMagicResistFormula

class StatsSystem:
    def __init__(self, world):
        self.world = world

        self.formulas = {
            Armor: BaseArmorFormula(),
            MagicResist: BaseMagicResistFormula(),
        }
    
    def update_modifiers(self, entity_id, stat_type): # TODO
        self.world.get_component(entity_id, stat_type).modifiers = []
    
    def update_base_values(self, entity_id):
        for stat_type in self.formulas:
            self.formulas[stat_type].calculate(self.world, entity_id)