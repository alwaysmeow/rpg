from typing import Dict, List, Set, Any
from dataclasses import dataclass

from engine.core.event import BaseEvent

from game.core.damage_type import DamageType
from game.core.statref import StatRef

@dataclass
class AttackEvent(BaseEvent):
    attacker_id: int
    target_id: int
    ability_id: int

@dataclass
class CastEvent(BaseEvent):
    caster_id: int
    target_id: int
    ability_id: int

class CastEvent(CastEvent): pass
class CastEndEvent(CastEvent): pass

@dataclass
class CooldownEvent(BaseEvent):
    ability_id: int

class CooldownSetEvent(CooldownEvent): pass
class CooldownUnsetEvent(CooldownEvent): pass

@dataclass
class CombatEvent(BaseEvent):
    combat_id: int
    teams: List[List[int]]

class CombatStartEvent(CombatEvent): pass
class CombatEndEvent(CombatEvent): pass

@dataclass
class DamageEvent(BaseEvent):
    source_id: int
    target_id: int
    damage_type: DamageType
    amount: int

@dataclass
class DeathEvent(BaseEvent):
    victim_id: int
    killer_id: int


@dataclass
class EffectEvent(BaseEvent):
    effect_id: int

class EffectApplyEvent(EffectEvent): pass
class EffectTickEvent(EffectEvent): pass
class EffectRemoveEvent(EffectEvent): pass

@dataclass
class StatsCreateEvent(BaseEvent):
    entity_id: int
    created: Set[Any]

@dataclass
class StatsUpdateEvent(BaseEvent):
    entity_id: int
    updated: Dict[StatRef, float]

@dataclass
class UseResourceEvent(BaseEvent):
    entity_id: int
    resource: Dict[type, int]