from shared.event import *

class Command:
    event_type: type = None
    priority = 0

    def execute(self, world):
        raise NotImplementedError
    
    def unique_key(self):
        return None

class AttackCommand(Command):
    event_type = AttackEvent
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world):
        return world.ability_system.attack(self.ability_id)

class CastStartCommand(Command):
    event_type = CastStartEvent
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world):
        return world.ability_system.cast_start(self.ability_id)

class CastEndCommand(Command):
    event_type = CastEndEvent
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world):
        return world.ability_system.cast_end(self.ability_id)

class DamageCommand(Command):
    event_type = DamageEvent
    priority = 5

    def __init__(self, source_id: int, target_id: int, damage_type, amount: float):
        self.source_id = source_id
        self.target_id = target_id
        self.damage_type = damage_type
        self.amount = amount

    def execute(self, world):
        return world.damage_system.damage(self.source_id, self.target_id, self.damage_type, self.amount)

class DeathCommand(Command):
    event_type = DeathEvent
    priority = 5

    def __init__(self, victim_id: int, killer_id: int):
        self.victim_id = victim_id
        self.killer_id = killer_id

    def execute(self, world):
        return world.damage_system.death(self.victim_id, self.killer_id)

class CombatStartCommand(Command):
    event_type = CombatStartEvent
    priority = 5

    def __init__(self, combat_id: int):
        self.combat_id = combat_id

    def execute(self, world):
        return world.combat_system.combat_start(self.combat_id)

class CombatEndCommand(Command):
    event_type = CombatEndEvent
    priority = 0

    def __init__(self, combat_id: int):
        self.combat_id = combat_id

    def execute(self, world):
        return world.combat_system.combat_end(self.combat_id)

    def unique_key(self):
        return (CombatEndCommand, self.combat_id)

class CooldownSetCommand(Command):
    event_type = CooldownSetEvent
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world):
        return world.cooldown_system.cooldown_set(self.ability_id)

class CooldownUnsetCommand(Command):
    event_type = CooldownUnsetEvent
    priority = 5

    def __init__(self, ability_id: int):
        self.ability_id = ability_id

    def execute(self, world):
        return world.cooldown_system.cooldown_unset(self.ability_id)

class StatsCreateCommand(Command):
    event_type = StatsCreateEvent
    priority = 10

    def __init__(self, entity_id: int, components: list):
        self.entity_id = entity_id
        self.components = components

    def execute(self, world):
        return world.cooldown_system.create_stats(self.entity_id, self.components)

class StatsUpdateCommand(Command):
    event_type = StatsUpdateEvent
    priority = 10

    def __init__(self, entity_id: int, statrefs: list):
        self.entity_id = entity_id
        self.statrefs = statrefs

    def execute(self, world):
        return world.cooldown_system.update_stats(self.entity_id, self.statrefs)