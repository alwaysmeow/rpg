from entity.modifier import apply_modifiers
from utils import clamp

class Meter:
    def __init__(self, max_value = 0, regen = 0):
        self.base_max_value = max_value
        self.max_value_modifiers = []

        self.base_regen = regen
        self.regen_modifiers = []

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

    @property
    def effective_max_value(self):
        return apply_modifiers(self.base_max_value, self.max_value_modifiers)

    @property
    def effective_regen(self):
        return apply_modifiers(self.base_regen, self.regen_modifiers)