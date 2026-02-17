from component.stats import Armor, MagicResist, Health, AttackDamage, AttackSpeed
from component.name import Name
from component.ability import AbilityEffect, Owner, Cooldown, CastTime, Autocast
from component.tag import Unit, Ability, Attack, TargetAbility

from abilities.attack import attack_handler

class EntitySystem:
    def __init__(self, world):
        self.world = world

    def create_unit(self, name):
        unit_id = self.world.create_entity()

        self.world.add_component(unit_id, Name(name))
        self.world.add_component(unit_id, Health(100, 0))
        self.world.add_component(unit_id, Armor(1))
        self.world.add_component(unit_id, MagicResist())
        self.world.add_component(unit_id, AttackDamage(10))
        self.world.add_component(unit_id, AttackSpeed(10))
        self.world.add_tag(unit_id, Unit)

        return unit_id
    
    def create_ability(self, owner, handler, cast_time, cooldown_duration, autocast):
        ability_id = self.world.create_entity()

        self.world.add_component(ability_id, AbilityEffect(handler))
        self.world.add_component(ability_id, Owner(owner))
        self.world.add_component(ability_id, CastTime(cast_time))
        self.world.add_component(ability_id, Cooldown(cooldown_duration, 1))
        self.world.add_component(ability_id, Autocast(autocast))
        
        self.world.add_tag(ability_id, Ability)

        return ability_id
    
    def create_autoattack(self, owner):
        ability_id = self.create_ability(owner, attack_handler, 0, 1, True)
        self.world.add_tag(ability_id, Attack)
        self.world.add_tag(ability_id, TargetAbility)

        return ability_id
