from engine.system.system import System
from engine.core.event import NoneEvent

from game.component.ability import Owner, CastTime, Cooldown, ResourceCost
from game.component.target import Target
from game.component.behaviour import CompositeBehaviour
from game.tag.tag import Dead, TargetAbility, Attack, Autocast

from game.core.command import *
from game.core.event import *

class AbilitySystem(System):
    def __init__(self, world):
        super().__init__(world)

        self.subscribe(CooldownUnsetEvent, self._on_cooldown_unset)
        self.subscribe(CombatStartEvent, self._on_combat_start)
    
    def attack(self, ability_id):
        attacker_id = self._get_caster_id(ability_id)
        target_id = self._get_target_id(attacker_id)
        self._invoke(ability_id, "on_attack")
        return AttackEvent(attacker_id, target_id, ability_id)

    def cast(self, ability_id):
        if self._is_cast_possible(ability_id):
            caster_id = self._get_caster_id(ability_id)
            target_id = self._get_target_id(caster_id)
            self._invoke(ability_id, "on_cast")
            return CastEvent(caster_id, target_id, ability_id)
        else:
            return NoneEvent()

    def cast_end(self, ability_id):
        caster_id = self._get_caster_id(ability_id)
        target_id = self._get_target_id(caster_id)
        self._invoke(ability_id, "on_cast_end")
        return CastEndEvent(caster_id, target_id, ability_id)

    def _invoke(self, ability_id, method_name):
        behaviour = self.world.get_component(ability_id, CompositeBehaviour)
        if behaviour:
            getattr(behaviour, method_name)(self.world, ability_id)

    def _get_caster_id(self, ability_id):
        caster = self.world.get_component(ability_id, Owner)
        if caster:
            return caster.unit_id
        else:
            return None

    def _get_target_id(self, caster_id):
        target = self.world.get_component(caster_id, Target)
        if target:
            return target.unit_id
        else:
            return None

    def _get_cost(self, ability_id):
        cost = self.world.get_component(ability_id, ResourceCost)
        if cost:
            return cost.cost
        else:
            return {}

    def _is_cast_possible(self, ability_id):
        caster_id = self._get_caster_id(ability_id)
        target_id = self._get_target_id(caster_id)
        ability_tags = self.world.get_tags(ability_id)

        # Check cooldown
        if not self._is_ability_ready(ability_id):
            self.world.logger.error("Spell is not ready. Cast isn't possible.")
            return False

        # Check is caster alive
        if caster_id and self.world.has_tag(caster_id, Dead):
            self.world.logger.error("Caster should be alive. Cast isn't possible.")
            return False

        # Check target if it's target ability
        if TargetAbility in ability_tags and target_id is None:
            self.world.logger.error("Casting of this ability needs target. Cast isn't possible.")
            return False
        
        # Check resources
        if not self._enough_resources(ability_id):
            self.world.logger.error("Not enough resources. Cast isn't possible.")
            return False

        return True

    def _is_ability_ready(self, ability_id):
        cooldown = self.world.get_component(ability_id, Cooldown)
        return not cooldown or cooldown.value >= 1
    
    def _enough_resources(self, ability_id):
        cost = self._get_cost(ability_id)
        caster_id = self._get_caster_id(ability_id)

        for resource_type in cost:
            resource_component = self.world.get_component(caster_id, resource_type)

            if not resource_component or resource_component.value < cost[resource_type]:
                return False

        return True

    def _autocast_trigger(self, ability_id):
        if self.world.has_tag(ability_id, Autocast):
            command_type = self._cast_command_type(ability_id)
            self.schedule(command_type(ability_id))

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