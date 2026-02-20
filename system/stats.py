from typing import Set

from component.stats import Stats
from shared.statref import StatRef

class StatsSystem:
    def __init__(self, world):
        self.world = world
    
    def update_modifiers(self, entity_id, stat_type): # TODO
        self.world.get_component(entity_id, stat_type).modifiers = []

    def _update_stats(self, entity_id, stats: list[StatRef]):
        update_list = set(stats)

        # Circular dependency possible
        max_iterations = 15 # TODO: get from config
        iterations = 0

        while update_list and iterations < max_iterations:
            for stat_ref in update_list:
                self._update_stat_value(entity_id, stat_ref)

            update_list = self._get_children(entity_id, update_list)
            iterations += 1

    def _get_children(self, entity_id, parents: list[StatRef]) -> Set[StatRef]:
        # Gets StatRef's dependent on list of parent StatRef's
        stats_component = self.world.get_component(entity_id, Stats)

        if stats_component is None:
            self.world.logger.error(f"Entity {entity_id} has no stats")
            return set()
        
        child_stats: Set[StatRef] = set()

        stats = stats_component.set
        for component_type in stats:
            stat_component = self.world.get_component(entity_id, component_type)

            if not hasattr(stat_component, 'formulas'):
                continue

            for parent in parents:
                for child in self._get_component_children(stat_component, parent):
                    child_stats.add(child)
        
        return child_stats

    def _get_component_children(self, component, parent: StatRef) -> Set[StatRef]:
        # Gets StatRef's of component's values dependent on parent StatRef
        value_data_list: Set[StatRef] = set()

        for value_name in component.formulas:
            formula = component.formulas[value_name]
            requirements = formula.requires

            if parent in requirements:
                value_data_list.add(StatRef(type(component), value_name))
        
        return value_data_list

    def _update_stat_value(self, entity_id, stat_ref: StatRef):
        component = self.world.get_component(entity_id, stat_ref.component_type)

        if component is None:
            self.world.logger.error(f"Entity {entity_id} has no {stat_ref.component_type.__name__}")
            return

        formula = component.formulas[stat_ref.value_name]

        setattr(
            component, 
            stat_ref.value_name, 
            self._calculate_formula(entity_id, formula)
        )

    def _calculate_formula(self, unit_id, formula):
        kwargs = {}

        for require in formula.requires:
            component = self.world.get_component(unit_id, require.component_type)
            if component is None or not hasattr(component, require.value_name):
                self.world.logger.error(
                    f"{formula.__name__} requires {require.component_type.__name__}.{require.value_name}"
                )
                return 0
            
            arg_name = f"{require.component_type.formula_key}_{require.value_name}"
            kwargs[arg_name] = getattr(component, require.value_name)
        
        return formula.calculate(**kwargs)