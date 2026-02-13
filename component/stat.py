from entity.modifier import apply_modifiers

class Stat:
    def __init__(self, value = 0):
        self.base_value = value
        self.modifiers = []

    @property
    def effective_value(self):
        return apply_modifiers(self.base_value, self.modifiers)