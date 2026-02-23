from typing import Dict, List, Set, Any

from dataclasses import dataclass
from shared.damage_type import DamageType
from shared.statref import StatRef

@dataclass
class AttackEvent:
    attacker_id: int
    target_id: int
    ability_id: int

@dataclass
class CastEvent:
    caster_id: int
    target_id: int
    ability_id: int

class CastStartEvent(CastEvent): pass
class CastEndEvent(CastEvent): pass

@dataclass
class CooldownEvent:
    ability_id: int

class CooldownSetEvent(CooldownEvent): pass
class CooldownUnsetEvent(CooldownEvent): pass

@dataclass
class CombatEvent:
    combat_id: int
    teams: List[List[int]]

class CombatStartEvent(CombatEvent): pass
class CombatEndEvent(CombatEvent): pass

@dataclass
class DamageEvent:
    source_id: int
    target_id: int
    damage_type: DamageType
    amount: int

@dataclass
class DeathEvent:
    victim_id: int
    killer_id: int

@dataclass
class StatsCreateEvent:
    entity_id: int
    created: Set[Any]

@dataclass
class StatsUpdateEvent:
    entity_id: int
    updated: Dict[StatRef, float]