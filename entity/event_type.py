from enum import Enum

class EventType(Enum):
    ATTACK = "attack"
    CAST_END = "cast_end"
    CAST_START = "cast_start"
    COMBAT_END = "combat_end"
    COMBAT_START = "combat_start"
    COOLDOWN_END = "cooldown_end"
    DAMAGE = "damage"
    DEATH = "death"