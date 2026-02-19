from component.ability import AbilityEffect, Owner, CastTime, Cooldown, Autocast
from component.target import Target
from component.tag import Dead, TargetAbility, Attack

from shared.event_type import EventType
from shared.event_result import CastEventResult, CooldownEventResult, CombatEventResult

class AbilitySystem:
    def __init__(self, world):
        self.world = world

        self.world.events.subscribe(EventType.COOLDOWN_END, self._on_cooldown_end)
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

        ability_effect = self.world.get_component(ability_id, AbilityEffect).handler

        cast_time_component = self.world.get_component(ability_id, CastTime)
        cast_time = cast_time_component.value if cast_time_component else 0

        def cast_start_handler():
            return CastEventResult(caster_id, target_id, ability_id)

        def cast_end_handler():
            ability_effect(self.world, caster_id, target_id)
            if cooldown:
                cooldown.value = 0 # TODO: set cooldown event
            return CastEventResult(caster_id, target_id, ability_id)

        if cast_time:
            self.world.events.schedule(
                self.world.time.now, 
                cast_start_handler, 
                EventType.CAST_START
            )
        
        self.world.events.schedule(
            self.world.time.now + cast_time, 
            cast_end_handler, 
            self._event_type_on_cast(ability_id)
        )

        return True

    def _autocast_trigger(self, ability_id):
        autocast = self.world.get_component(ability_id, Autocast)
        if autocast and autocast.value:
            self.cast(ability_id)
    
    def _on_cooldown_end(self, cooldown_event_result: CooldownEventResult):
        self._autocast_trigger(cooldown_event_result.ability_id)
    
    def _on_combat_start(self, combat_start_event_result: CombatEventResult):
        for team in combat_start_event_result.teams:
            for unit_id in team:
                abilities = self.world.query_by_components({
                    Autocast: {
                        "include": { "value": [True] },
                    },
                    Owner: {
                        "include": { "unit_id": [unit_id] },
                    },
                })
                
                for ability_id in abilities:
                    self._autocast_trigger(ability_id)
    
    def _event_type_on_cast(self, ability_id):
        if self.world.has_tag(ability_id, Attack):
            return EventType.ATTACK
        else:
            return EventType.CAST_END