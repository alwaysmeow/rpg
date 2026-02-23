from typing import TypeVar, Generic, Type

from core.event import *

E = TypeVar("E", bound=BaseEvent)

class Command(Generic[E]):
    priority = 0

    def execute(self, world) -> E:
        raise NotImplementedError
    
    def unique_key(self):
        return None

class AttackCommand(Command[AttackEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> AttackEvent:
        return world.ability_system.attack(self.ability_id)

class CastStartCommand(Command[CastStartEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> CastStartEvent:
        return world.ability_system.cast_start(self.ability_id)

class CastEndCommand(Command[CastEndEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> CastEndEvent:
        return world.ability_system.cast_end(self.ability_id)

class DamageCommand(Command[DamageEvent]):
    priority = 5

    def __init__(self, source_id: int, target_id: int, damage_type, amount: float):
        self.source_id = source_id
        self.target_id = target_id
        self.damage_type = damage_type
        self.amount = amount

    def execute(self, world) -> DamageEvent:
        return world.damage_system.damage(self.source_id, self.target_id, self.damage_type, self.amount)

class DeathCommand(Command[DeathEvent]):
    priority = 5

    def __init__(self, victim_id: int, killer_id: int):
        self.victim_id = victim_id
        self.killer_id = killer_id

    def execute(self, world) -> DeathEvent:
        return world.damage_system.death(self.victim_id, self.killer_id)

class CombatStartCommand(Command[CombatStartEvent]):
    priority = 5

    def __init__(self, combat_id: int):
        self.combat_id = combat_id

    def execute(self, world) -> CombatStartEvent:
        return world.combat_system.combat_start(self.combat_id)

class CombatEndCommand(Command[CombatEndEvent]):
    priority = 0

    def __init__(self, combat_id: int):
        self.combat_id = combat_id

    def execute(self, world) -> CombatEndEvent:
        return world.combat_system.combat_end(self.combat_id)

    def unique_key(self):
        return (CombatEndCommand, self.combat_id)

class CooldownSetCommand(Command[CooldownSetEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> CooldownSetEvent:
        return world.cooldown_system.cooldown_set(self.ability_id)

class CooldownUnsetCommand(Command[CooldownUnsetEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> CooldownUnsetEvent:
        return world.cooldown_system.cooldown_unset(self.ability_id)

class StatsCreateCommand(Command[StatsCreateEvent]):
    priority = 10

    def __init__(self, entity_id: int, components: list):
        self.entity_id = entity_id
        self.components = components

    def execute(self, world) -> StatsCreateEvent:
        return world.stats_system.create_stats(self.entity_id, self.components)

class StatsUpdateCommand(Command[StatsUpdateEvent]):
    priority = 10

    def __init__(self, entity_id: int, statrefs: list):
        self.entity_id = entity_id
        self.statrefs = statrefs

    def execute(self, world) -> StatsUpdateEvent:
        return world.stats_system.update_stats(self.entity_id, self.statrefs)