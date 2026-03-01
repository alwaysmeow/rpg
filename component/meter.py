from utils import clamp

class Meter:
    formula_key = None

    def __init__(self, max_value = 0, regen = 0, base_max_value_formula: type = None, base_regen_formula: type = None, hardcoded: bool = False):
        self.base_max_value = max_value
        self.effective_max_value = max_value

        self.base_regen = regen
        self.effective_regen = regen

        self.formulas: dict[str, type] = {
            "base_max_value": base_max_value_formula,
            "base_regen": base_regen_formula,
        }

        self.hardcoded = hardcoded

        self._value_ratio = 1.0

    @property
    def value(self):
        return self._value_ratio * self.effective_max_value
    
    @value.setter
    def value(self, v):
        if self.effective_max_value == 0:
            self._value_ratio = 0
        else:
            self._value_ratio = clamp(v / self.effective_max_value, 0, 1)