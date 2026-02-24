from typing import TypeVar, Generic, Set, List

from core.event import *

# execute(self, world) methods of commands should use local import for preventing circular dependencies

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
        from system.ability import AbilitySystem
        return world.get_system(AbilitySystem).attack(self.ability_id)

class CastStartCommand(Command[CastStartEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> CastStartEvent:
        from system.ability import AbilitySystem
        return world.get_system(AbilitySystem).cast_start(self.ability_id)

class CastEndCommand(Command[CastEndEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> CastEndEvent:
        from system.ability import AbilitySystem
        return world.get_system(AbilitySystem).cast_end(self.ability_id)

class DamageCommand(Command[DamageEvent]):
    priority = 5

    def __init__(self, source_id: int, target_id: int, damage_type, amount: float):
        self.source_id = source_id
        self.target_id = target_id
        self.damage_type = damage_type
        self.amount = amount

    def execute(self, world) -> DamageEvent:
        from system.damage import DamageSystem
        return world.get_system(DamageSystem).damage(self.source_id, self.target_id, self.damage_type, self.amount)

class DeathCommand(Command[DeathEvent]):
    priority = 5

    def __init__(self, victim_id: int, killer_id: int):
        self.victim_id = victim_id
        self.killer_id = killer_id

    def execute(self, world) -> DeathEvent:
        from system.damage import DamageSystem
        return world.get_system(DamageSystem).death(self.victim_id, self.killer_id)

class CombatStartCommand(Command[CombatStartEvent]):
    priority = 0

    def __init__(self, combat_id: int):
        self.combat_id = combat_id

    def execute(self, world) -> CombatStartEvent:
        from system.combat import CombatSystem
        return world.get_system(CombatSystem).combat_start(self.combat_id)

class CombatEndCommand(Command[CombatEndEvent]):
    priority = 0

    def __init__(self, combat_id: int):
        self.combat_id = combat_id

    def execute(self, world) -> CombatEndEvent:
        from system.combat import CombatSystem
        return world.get_system(CombatSystem).combat_end(self.combat_id)

    def unique_key(self):
        return (CombatEndCommand, self.combat_id)

class CooldownSetCommand(Command[CooldownSetEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> CooldownSetEvent:
        from system.cooldown import CooldownSystem
        return world.get_system(CooldownSystem).cooldown_set(self.ability_id)

class CooldownUnsetCommand(Command[CooldownUnsetEvent]):
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world) -> CooldownUnsetEvent:
        from system.cooldown import CooldownSystem
        return world.get_system(CooldownSystem).cooldown_unset(self.ability_id)

class StatsCreateCommand(Command[StatsCreateEvent]):
    priority = 15

    def __init__(self, entity_id: int, components: List):
        self.entity_id = entity_id
        self.components = components

    def execute(self, world) -> StatsCreateEvent:
        from system.stats.stats import StatsSystem
        return world.get_system(StatsSystem).create_stats(self.entity_id, self.components)

class StatsUpdateCommand(Command[StatsUpdateEvent]):
    priority = 10

    def __init__(self, entity_id: int, statrefs: Set):
        self.entity_id = entity_id
        self.statrefs = statrefs

    def execute(self, world) -> StatsUpdateEvent:
        from system.stats.stats import StatsSystem
        return world.get_system(StatsSystem).update_stats(self.entity_id, self.statrefs)