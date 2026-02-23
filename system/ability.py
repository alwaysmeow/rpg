from component.ability import AbilityEffect, Owner, CastTime, Cooldown
from component.target import Target
from component.tag import Dead, TargetAbility, Attack, Autocast

from shared.command import *
from shared.event import *

class AbilitySystem:
    def __init__(self, world):
        self.world = world

        self.world.events.bus.subscribe(CooldownUnsetEvent, self._on_cooldown_unset)
        self.world.events.bus.subscribe(CombatStartEvent, self._on_combat_start)
    
    def attack(self, ability_id):
        attacker_id, target_id = self._cast(ability_id, AttackCommand)
        ability_handler = self.world.get_component(ability_id, AbilityEffect).handler
        ability_handler(self.world, attacker_id, target_id)
        return AttackEvent(attacker_id, target_id, ability_id)

    def cast_start(self, ability_id):
        caster_id, target_id = self._cast(ability_id, CastStartCommand)
        return CastStartEvent(caster_id, target_id, ability_id)

    def cast_end(self, caster_id, target_id, ability_id):
        ability_handler = self.world.get_component(ability_id, AbilityEffect).handler
        ability_handler(self.world, caster_id, target_id)
        return CastEndEvent(caster_id, target_id, ability_id)

    def _cast(self, ability_id, command_type):
        ability_tags = self.world.get_tags(ability_id)

        cooldown = self.world.get_component(ability_id, Cooldown)
        if cooldown and cooldown.value != 1:
            self.world.logger.error("Spell is not ready. Cast cancelled.")
            return None, None

        caster_id = None
        caster = self.world.get_component(ability_id, Owner)
        if caster:
            caster_id = caster.unit_id

        if caster_id and self.world.has_tag(caster_id, Dead):
            self.world.logger.error("Caster should be alive. Cast cancelled.")
            return None, None

        target_id = None
        target = self.world.get_component(caster_id, Target)
        if target:
            target_id = target.unit_id

        if TargetAbility in ability_tags and target_id is None:
            self.world.logger.error("Casting of this ability needs target. Cast cancelled.")
            return None, None

        cast_time_component = self.world.get_component(ability_id, CastTime)
        cast_time = cast_time_component.value if cast_time_component else 0

        self.world.events.scheduler.schedule(
            self.world.time.now,
            CooldownSetCommand(ability_id)
        )

        return caster_id, target_id

    def _autocast_trigger(self, ability_id):
        if self.world.has_tag(ability_id, Autocast):
            command_type = self._cast_command_type(ability_id)
            self.world.events.scheduler.schedule(
                self.world.time.now,
                command_type(ability_id)
            )
    
    def _on_cooldown_unset(self, cooldown_event_result: CooldownEvent):
        self._autocast_trigger(cooldown_event_result.ability_id)
    
    def _on_combat_start(self, combat_start_event_result: CombatStartEvent):
        for team in combat_start_event_result.teams:
            for unit_id in team:
                abilities = self.world.query_by_component(
                    Owner,
                    include_filters = { "unit_id": [unit_id] }
                )
                
                for ability_id in abilities:
                    self._autocast_trigger(ability_id)
    
    def _cast_command_type(self, ability_id):
        if self.world.has_tag(ability_id, Attack):
            return AttackCommand
        else:
            return CastEndCommand
    
    def _switch_autocast(self, ability_id):
        if self.world.has_tag(ability_id, Autocast):
            self.world.remove_tag(ability_id, Autocast)
        else:
            self.world.add_tag(ability_id, Autocast)