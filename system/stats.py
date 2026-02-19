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

        for require in formula.requires:
            component_type, value_name = require

            component = self.world.get_component(unit_id, component_type)
            if component is None or not hasattr(component, value_name):
                self.world.logger.error(f"{formula.__name__} requires {component_type.__name__}.{value_name}")
                return 0
            
            arg_name = f"{component_type.__name__.lower()}_{value_name}"
            kwargs[arg_name] = getattr(component, value_name)
        
        return formula.calculate(**kwargs)