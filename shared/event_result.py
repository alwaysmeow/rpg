from dataclasses import dataclass
from shared.damage_type import DamageType
from shared.statref import StatRef

@dataclass
class AttackEventResult:
    attacker_id: int
    target_id: int
    ability_id: int

@dataclass
class CastEventResult:
    caster_id: int
    target_id: int
    ability_id: int

@dataclass
class CooldownEventResult:
    ability_id: int

@dataclass
class CombatEventResult:
    combat_id: int
    teams: list[list[int]]

@dataclass
class DamageEventResult:
    source_id: int
    target_id: int
    amount: int
    damage_type: DamageType

@dataclass
class DeathEventResult:
    victim_id: int
    killer_id: int

@dataclass
class StatUpdateResult:
    entity_id: int
    statref: StatRef
    new_value: float
    depth: int = 0