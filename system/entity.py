from component.stats import Armor, MagicResist, Health
from component.name import Name
from component.combat import CombatParticipants, CombatState
from component.ability import AbilityEffect, Owner, Cooldown, CastTime
from component.tag import Unit, Combat, Ability, AutoAttack

class EntitySystem:
    def __init__(self, world):
        self.world = world

    def create_unit(self, name):
        unit_id = self.world.create_entity()

        self.world.add_component(unit_id, Name(name))
        self.world.add_component(unit_id, Health(100, 0))
        self.world.add_component(unit_id, Armor())
        self.world.add_component(unit_id, MagicResist())
        self.world.add_tag(unit_id, Unit)

        return unit_id
    
    def create_combat(self, team1, team2):
        combat_id = self.world.create_entity()

        self.world.add_component(combat_id, CombatState())
        self.world.add_component(combat_id, CombatParticipants(team1, team2))
        self.world.add_tag(combat_id, Combat)

        return combat_id
    
    def create_ability(self, owner, effect, cast_time, cooldown_duration):
        ability_id = self.world.create_entity()

        self.world.add_component(ability_id, AbilityEffect(effect))
        self.world.add_component(ability_id, Owner(owner))
        self.world.add_component(ability_id, CastTime(cast_time))
        self.world.add_component(ability_id, Cooldown(cooldown_duration, 1))
        
        self.world.add_tag(ability_id, Ability)

        return ability_id
    
    def create_autoattack(self, owner):
        ability_id = self.create_ability(owner, None, 1) # TODO: create autoattack effect
        self.world.add_tag(ability_id, AutoAttack)
