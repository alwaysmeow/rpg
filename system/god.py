from system.time import TimeSystem
from system.event.event import EventSystem

from component.stats import Stats, Armor, MagicResistance, Health, AttackDamage, AttackSpeed, AttackDelay
from component.name import Name
from component.ability import AbilityEffect, Owner, Cooldown, CastTime
from tag.tag import Unit, Ability, Attack, TargetAbility, Autocast

from core.command import *
from core.formula import AttackDelayFormula

from abilities.attack import attack_handler

class God:
    def __init__(self, world):
        self.world = world

    def create_unit(self, name):
        unit_id = self.world.create_entity()

        self.world.add_component(unit_id, Name(name))
        
        self.exec_cmd(
            StatsCreateCommand(
                unit_id, 
                [
                    Health(100, 0),
                    Armor(1),
                    MagicResistance(),
                    AttackDamage(10),
                ]
            )
        )

        self.world.add_tag(unit_id, Unit)

        return unit_id
    
    def create_ability(self, owner, handler, cast_time, cooldown_duration, autocast):
        ability_id = self.world.create_entity()

        self.world.add_component(ability_id, AbilityEffect(handler))
        self.world.add_component(ability_id, Owner(owner))
        self.world.add_component(ability_id, CastTime(cast_time))
        self.world.add_component(ability_id, Cooldown(cooldown_duration, 1))

        self.world.add_tag(ability_id, Ability)
        if autocast:
            self.world.add_tag(ability_id, Autocast)

        return ability_id
    
    def create_autoattack(self, owner_id, attack_speed_value):
        ability_id = self.create_ability(owner_id, attack_handler, 0, 1, True)
        self.world.add_tag(ability_id, Attack)
        self.world.add_tag(ability_id, TargetAbility)

        self.exec_cmd(
            StatsCreateCommand(
                owner_id, 
                [
                    AttackSpeed(attack_speed_value),
                    AttackDelay(None, AttackDelayFormula)
                ]
            )
        )

        return ability_id
    
    def exec_cmd(self, command):
        self.world.get_system(EventSystem).scheduler.schedule(
            self.world.get_system(TimeSystem).now,
            command
        )