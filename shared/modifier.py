from enum import Enum

# Legacy

def apply_modifiers(base_value, modifiers):
    flat = 0
    multiplier = 0
    for modifier in modifiers:
        match modifier.type:
            case ModifierType.Flat:
                flat += modifier.value
            case ModifierType.Multiplier:
                multiplier += modifier.value
    return (base_value + flat) * (1 + multiplier)

class ModifierType(Enum):
    Flat = 0
    Multiplier = 1