from typing import Set, Dict

from component.stat import Stat
from component.meter import Meter
from component.stats import Stats, AttackSpeed, AttackDelay

from core.statref import StatRef
from core.command import StatsUpdateCommand
from core.event import StatsCreateEvent, StatsUpdateEvent

from system.system import System
from system.stats.formula import FormulaSystem
from system.stats.modifier import ModifierSystem

class StatsSystem(System):
    def __init__(self, world):
        super().__init__(world)

        self.formulas = FormulaSystem(world)
        self.modifiers = ModifierSystem(world)

        self.base_to_effective_names = {
            "base_value": "effective_value",
            "base_max_value": "effective_max_value",
            "base_regen": "effective_regen"
        }

    def create_stats(self, entity_id, components) -> StatsCreateEvent:
        statrefs = set()
        for component in components:
            statrefs |= self._create_stat(entity_id, component)

        self.schedule(StatsUpdateCommand(entity_id, statrefs))

        return StatsCreateEvent(entity_id, components)

    def update_stats(self, entity_id, statrefs: Set[StatRef]) -> StatsUpdateEvent:
        pending_statrefs = statrefs.copy()
        updated = {}

        # Circular dependency possible
        max_iterations = 15 # TODO: get from config
        iterations = 0

        while pending_statrefs and iterations < max_iterations:
            updated |= self._stats_update_round(entity_id, pending_statrefs)

            pending_statrefs = self._resolve_dependencies(entity_id, pending_statrefs)
            iterations += 1
        
        return StatsUpdateEvent(entity_id, updated)

    def _resolve_dependencies(self, entity_id, parents: Set[StatRef]) -> Set[StatRef]:
        # Gets StatRef's dependent set of parent StatRef's
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
                for child in self._get_statref_children_from_component(stat_component, parent):
                    child_stats.add(child)
        
        return child_stats

    def _get_statref_children_from_component(self, component, parent: StatRef) -> Set[StatRef]:
        # Gets StatRef's of component's values dependent on parent StatRef
        value_data_list: Set[StatRef] = set()

        for value_name in component.formulas:
            formula = component.formulas[value_name]

            if formula is None:
                continue

            requirements = formula.requires

            if parent in requirements:
                value_data_list.add(StatRef(type(component), value_name))
        
        return value_data_list

    def _stats_update_round(self, entity_id, statrefs: Set[StatRef]) -> Dict[StatRef, float]:
        base_values_names = self.base_to_effective_names.keys()
        effective_values_names = self.base_to_effective_names.values()

        base_statrefs = set(s for s in statrefs if s.value_name in base_values_names)
        effective_statrefs = set(s for s in statrefs if s.value_name in effective_values_names)

        updated = {}

        # Base values updating
        for statref in base_statrefs:
            new_value = self.formulas._update_formula_value(entity_id, statref)
            updated[statref] = new_value

            # Update effective values of updated base values
            effective_name = self.base_to_effective_names[statref.value_name]
            effective_statref = StatRef(statref.component_type, effective_name)
            effective_statrefs.add(effective_statref)

        # Effective values updating
        for statref in effective_statrefs:
            new_value = self.modifiers._update_effective_value(entity_id, statref)
            updated[statref] = new_value

        return updated
    
    def _get_statrefs_of_base_values(self, component) -> Set[StatRef]: # TODO: rework
        statrefs = set()

        if isinstance(component, Stat):
            statrefs.add(StatRef(type(component), "base_value"))
        elif isinstance(component, Meter):
            statrefs.add(StatRef(type(component), "base_max_value"))
            statrefs.add(StatRef(type(component), "base_regen"))
        
        return statrefs
    
    def _create_stat(self, entity_id, component):
        self.world.add_component(entity_id, component)
        stat_type = type(component)

        stats = self.world.get_or_create_component(entity_id, Stats)
        stats.add(stat_type)

        statrefs = self._get_statrefs_of_base_values(component)
        return statrefs