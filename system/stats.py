from component.stats import Stats
from component.stat import FormulaStat
from component.meter import FormulaMeter

class StatsSystem:
    def __init__(self, world):
        self.world = world
    
    def update_modifiers(self, entity_id, stat_type): # TODO
        self.world.get_component(entity_id, stat_type).modifiers = []

    def _on_stat_update(self, entity_id, update_list: list[tuple]):
        stats_component = self.world.get_component(entity_id, Stats)

        if stats_component in None:
            self.world.logger.error(f"Entity {entity_id} has no {component_type.__name__}")
            return
        
        to_update_list = []

        stats = stats_component.set
        for component_type in stats:
            stat_component = self.world.get_component(entity_id, component_type)

            for updated_value in update_list:
                to_update_list.append(*self._dependent_component_values(stat_component, updated_value))
        
        return update_list

    def _dependent_component_values(self, component, stat_value_data: tuple):
        value_data_list: list[tuple] = []

        if isinstance(component, FormulaMeter):
            pass
        elif isinstance(component, FormulaStat):
            requirements = component.base_value_formula.requires
            if stat_value_data in requirements:
                value_data_list.append((type(component), "base_value"))
        
        return value_data_list

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

        return component_type

    def _calculate_formula(self, unit_id, formula):
        kwargs = {}

        for require in formula.requires:
            component_type, value_name = require

            component = self.world.get_component(unit_id, component_type)
            if component is None or not hasattr(component, value_name):
                self.world.logger.error(f"{formula.__name__} requires {component_type.__name__}.{value_name}")
                return 0
            
            arg_name = f"{component_type.formula_key}_{value_name}"
            kwargs[arg_name] = getattr(component, value_name)
        
        return formula.calculate(**kwargs)