class Stat:
    formula_key = None

    def __init__(self, value = 0):
        self.base_value = value
        self.effective_value = value

class FormulaStat(Stat):
    def __init__(self, value = 0, formula: type = None):
        super().__init__(value)
        self.formulas: dict[str, type] = {
            "base_value": formula
        }