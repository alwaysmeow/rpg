class Stat:
    formula_key = None

    def __init__(self, value = 0, formula: type = None, hardcoded: bool = False):
        self.base_value = value
        self.effective_value = value
        self.formulas: dict[str, type] = {
            "base_value": formula
        }
        self.hardcoded = hardcoded