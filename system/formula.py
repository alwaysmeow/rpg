from shared.statref import StatRef

class FormulaSystem:
    def __init__(self, world):
        self.world = world

    def _update_formula_value(self, entity_id, stat_ref: StatRef):
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

    def _calculate_formula(self, entity_id, formula):
        kwargs = {}

        for require in formula.requires:
            component = self.world.get_component(entity_id, require.component_type)
            if component is None or not hasattr(component, require.value_name):
                self.world.logger.error(
                    f"{formula.__name__} requires {require.component_type.__name__}.{require.value_name}"
                )
                return 0
            
            arg_name = f"{require.component_type.formula_key}_{require.value_name}"
            kwargs[arg_name] = getattr(component, require.value_name)
        
        return formula.calculate(**kwargs)