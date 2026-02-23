from component.ability import AbilityEffect, Owner, CastTime, Cooldown
from component.target import Target
from component.tag import Dead, TargetAbility, Attack, Autocast

from shared.event_type import EventType
from shared.event_result import CastEventResult, CooldownEventResult, CombatEventResult, AttackEventResult

class AbilitySystem:
    def __init__(self, world):
        self.world = world

        self.world.events.subscribe(EventType.COOLDOWN_UNSET, self._on_cooldown_unset)
        self.world.events.subscribe(EventType.COMBAT_START, self._on_combat_start)
    
    def cast(self, ability_id):
        ability_tags = self.world.get_tags(ability_id)

        cooldown = self.world.get_component(ability_id, Cooldown)
        if cooldown and cooldown.value != 1:
            self.world.logger.error("Spell is not ready. Cast cancelled.")
            return False

        caster_id = None
        caster = self.world.get_component(ability_id, Owner)
        if caster:
            caster_id = caster.unit_id

        if caster_id and self.world.has_tag(caster_id, Dead):
            self.world.logger.error("Caster should be alive. Cast cancelled.")
            return False

        target_id = None
        target = self.world.get_component(caster_id, Target)
        if target:
            target_id = target.unit_id

        if TargetAbility in ability_tags and target_id is None:
            self.world.logger.error("Casting of this ability needs target. Cast cancelled.")
            return False

        cast_time_component = self.world.get_component(ability_id, CastTime)
        cast_time = cast_time_component.value if cast_time_component else 0

        def cast_start_handler():
            return CastEventResult(caster_id, target_id, ability_id)

        if cast_time:
            self.world.events.schedule(
                self.world.time.now, 
                cast_start_handler, 
                EventType.CAST_START
            )
        
        self.world.events.schedule(
            self.world.time.now + cast_time, 
            self._create_cast_end_handler(caster_id, target_id, ability_id), 
            self._event_type_on_cast(ability_id)
        )

        return True

    def cast_end(self, caster_id, target_id, ability_id):
        ability_handler = self.world.get_component(ability_id, AbilityEffect).handler

        if self.world.has_tag(ability_id, Attack):
            ability_handler(self.world, caster_id, target_id)
            return AttackEventResult(caster_id, target_id, ability_id)
        else:
            ability_handler(self.world, caster_id, target_id)
            return CastEventResult(caster_id, target_id, ability_id)

    def _autocast_trigger(self, ability_id):
        if self.world.has_tag(ability_id, Autocast):
            self.cast(ability_id)
    
    def _on_cooldown_unset(self, cooldown_event_result: CooldownEventResult):
        self._autocast_trigger(cooldown_event_result.ability_id)
    
    def _on_combat_start(self, combat_start_event_result: CombatEventResult):
        for team in combat_start_event_result.teams:
            for unit_id in team:
                abilities = self.world.query_by_component(
                    Owner,
                    include_filters = { "unit_id": [unit_id] }
                )
                
                for ability_id in abilities:
                    self._autocast_trigger(ability_id)
    
    def _event_type_on_cast(self, ability_id):
        if self.world.has_tag(ability_id, Attack):
            return EventType.ATTACK
        else:
            return EventType.CAST_END
    
    def _create_cast_end_handler(self, caster_id, target_id, ability_id):
        ability_handler = self.world.get_component(ability_id, AbilityEffect).handler

        if self.world.has_tag(ability_id, Attack):
            def cast_end_handler():
                ability_handler(self.world, caster_id, target_id)
                return AttackEventResult(caster_id, target_id, ability_id)
        else: 
            def cast_end_handler():
                ability_handler(self.world, caster_id, target_id)
                return CastEventResult(caster_id, target_id, ability_id)

        return cast_end_handler
    
    def _switch_autocast(self, ability_id):
        if self.world.has_tag(ability_id, Autocast):
            self.world.remove_tag(ability_id, Autocast)
        else:
            self.world.add_tag(ability_id, Autocast)