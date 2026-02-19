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

    def _calculate_formula(self, unit_id, formula):
        kwargs = {}

        for component_type in formula.requires:
            component = self.world.get_component(unit_id, component_type)
            if not component:
                self.world.logger.error(f"Unit has no {component_type.__name__} for calculating {formula.__name__}")
                return 0
            kwargs[component_type.__name__.lower()] = component
        
        return formula.calculate(**kwargs)