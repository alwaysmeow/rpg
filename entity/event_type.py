from enum import Enum

class EventType(Enum):
    ATTACK = "on_attack"
    CAST_START = "on_cast_start"
    CAST_END = "on_cast_end"
    COOLDOWN_END = "on_cooldown_end"
    DAMAGE = "on_damage"
    DEATH = "on_death"