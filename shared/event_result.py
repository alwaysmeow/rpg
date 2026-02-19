from dataclasses import dataclass
from shared.damage_type import DamageType

@dataclass
class AttackEventResult:
    attacker_id: int
    target_id: int

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