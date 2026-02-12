from entity.modifier import ModifierType

class Stat:
    def __init__(self, value = 0):
        self.base_value = value
        self.modifiers = []

    @property
    def effective_value(self):
        flat = 0
        multiplier = 0
        for modifier in self.modifiers:
            match modifier.type:
                case ModifierType.Flat:
                    flat += modifier.value
                case ModifierType.Multiplier:
                    mult += modifier.value
        return (self.base_value + flat) * (1 + multiplier)