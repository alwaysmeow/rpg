from shared.modifier import apply_modifiers

class Stat:
    def __init__(self, value = 0):
        self.base_value = value
        self.modifiers = []

    @property
    def effective_value(self):
        return apply_modifiers(self.base_value, self.modifiers)

class FormulaStat(Stat):
    def __init__(self, value = 0, formula: type = None):
        super().__init__(value)
        self.base_value_formulas: type = formula