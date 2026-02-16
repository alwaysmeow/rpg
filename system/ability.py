from component.ability import AbilityEffect, Owner, CastTime, Cooldown
from component.target import Target
from component.tag import Dead, TargetAbility

class AbilitySystem:
    def __init__(self, world):
        self.world = world
    
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

        if TargetAbility in ability_tags and not target_id:
            self.world.logger.error("Casting of this ability needs target. Cast cancelled.")
            return False

        ability_effect = self.world.get_component(ability_id, AbilityEffect).handler

        cast_time_component = self.world.get_component(ability_id, CastTime)
        cast_time = cast_time_component.value if cast_time_component else 0

        def handler():
            ability_effect(self.world, caster_id, target_id)
            if cooldown:
                cooldown.value = 0

        self.world.events.schedule(self.world.time.now + cast_time, handler)

        return True