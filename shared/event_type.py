from enum import Enum

class EventType(Enum):
    ATTACK = ("attack", 5)
    CAST_START = ("cast_start", 5)
    CAST_END = ("cast_end", 5)
    DAMAGE = ("damage", 5)
    DEATH = ("death", 5)
    COMBAT_START = ("combat_start", 5)
    COMBAT_END = ("combat_end", 0)
    COOLDOWN_SET = ("cooldown_set", 5)
    COOLDOWN_UNSET = ("cooldown_unset", 5)
    STATS_CREATE = ("stat_create", 10)
    STATS_UPDATE = ("stat_update", 10)

    def __init__(self, value, priority):
        self._value_ = value
        self.priority = priority