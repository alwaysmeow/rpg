from component.stats import Armor, MagicResist
from shared.formula import BaseArmorFormula, BaseMagicResistFormula

class StatsSystem:
    def __init__(self, world):
        self.world = world
    
    def update_modifiers(self, entity_id, stat_type): # TODO
        self.world.get_component(entity_id, stat_type).modifiers = []

    def update_stat(self, entity_id, component_type, value_name):
        component = self.world.get_component(entity_id, component_type)

        if component is None:
            self.world.logger.error(f"Entity {entity_id} has no {component_type.__name__}")
            return

        formula_attr_name = f"{value_name}_formula"
        formula = getattr(component, formula_attr_name)

        setattr(
            component, 
            value_name, 
            self._calculate_formula(entity_id, formula)
        )

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