from engine.system.time import TimeSystem
from engine.system.event.event import EventSystem

from game.component.stats import Health
from game.component.ability import Owner, Cooldown, CastTime
from game.component.behaviour import CompositeBehaviour
from game.component.effect import EffectTarget, EffectDuration, Effects
from game.tag.tag import Ability, Attack, TargetAbility, Autocast

from game.core.command import *
from game.core.formula import AttackDelayFormula

from game.behaviour.abilities.attack import AttackBehaviour
from game.behaviour.abilities.resource_restore import ResourceRestoreBehaviour
from game.behaviour.effects.damage_over_time import DamageOverTimeBehaviour

class God:
    def __init__(self, world):
        self.world = world
    
    def create_ability(self, owner, behaviours, cast_time, cooldown_duration, autocast):
        ability_id = self.world.create_entity()

        self.world.add_component(ability_id, CompositeBehaviour(*behaviours))
        self.world.add_component(ability_id, Owner(owner))
        self.world.add_component(ability_id, CastTime(cast_time))
        self.world.add_component(ability_id, Cooldown(cooldown_duration, 1))

        self.world.add_tag(ability_id, Ability)
        if autocast:
            self.world.add_tag(ability_id, Autocast)

        return ability_id
    
    def create_autoattack(self, owner_id):
        ability_id = self.create_ability(
            owner_id, 
            [
                AttackBehaviour(),
                ResourceRestoreBehaviour({ Health: 10 })
            ], 
            0, 1, True
        )
        self.world.add_tag(ability_id, Attack)
        self.world.add_tag(ability_id, TargetAbility)
        return ability_id
    
    def create_dot_effect(self, target_id, damage, delay):
        effect_id = self.world.create_entity()

        self.world.add_component(effect_id, EffectTarget(target_id))
        self.world.add_component(effect_id, EffectDuration(None))
        self.world.add_component(effect_id, CompositeBehaviour(
            DamageOverTimeBehaviour(DamageType.Pure, damage, delay)
        ))

        effects = self.world.get_or_create_component(target_id, Effects)
        effects.set.add(effect_id)

        self.exec_cmd(EffectApplyCommand(effect_id))

    def exec_cmd(self, command):
        self.world.get_system(EventSystem).scheduler.schedule(
            self.world.get_system(TimeSystem).now,
            command
        )