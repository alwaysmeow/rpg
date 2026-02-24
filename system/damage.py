from random import random
from dataclasses import dataclass

from system.system import System

from utils import load_config
from component.stats import Health, MagicResistance, Armor
from tag.tag import Dead

from core.damage_type import DamageType
from core.command import *
from core.event import DamageEvent, DeathEvent

@dataclass
class Damage: # similar to DamageEvent
    source_id: int
    target_id: int
    type: DamageType
    amount: int

class DamageSystem(System):
    def __init__(self, world, game_config_path="config/game.json"):
        super().__init__(world)

        config = load_config(game_config_path)
        self.armor_coefficient = config["armor_coefficient"]
    
    def damage(self, source_id, target_id, damage_type, base_amount):
        damage = Damage(source_id, target_id, damage_type, base_amount)
        amount = self._process_damage(damage)
        return DamageEvent(source_id, target_id, damage_type, amount)
    
    def death(self, victim_id, killer_id):
        self.world.add_tag(victim_id, Dead)
        return DeathEvent(victim_id, killer_id)

    def _process_damage(self, damage: Damage):
        health = self.world.get_component(damage.target_id, Health)
        if not health:
            self.world.logger.error("Target has no health. Damage processing cancelled.")
            return 0
         
        amount = damage.amount

        amount = self._apply_modifiers(damage, amount)
        amount = self._apply_resistance(damage, amount)
        amount = self._round_amount(amount)
        amount = self._apply_for_unit(damage.target_id, amount)

        if self._check_death(damage.target_id):
            self.schedule(DeathCommand(damage.target_id, damage.source_id))
        
        return round(amount)

    def _apply_modifiers(self, damage, amount):
        # TODO: modifiers processing
        return amount
    
    def _reduced_physical_damage(self, amount, target_id):
        armor = self.world.get_component(target_id, Armor)

        if not armor:
            return amount
        else:
            coefficient = self.armor_coefficient ** armor.effective_value # TODO: analyze formula
            return amount * coefficient

    def _reduced_magic_damage(self, amount, target_id):
        magic_resist = self.world.get_component(target_id, MagicResistance)

        if not magic_resist:
            return amount
        else:
            coefficient = 1 - magic_resist.effective_value
            return amount * coefficient

    def _apply_resistance(self, damage, amount):
        match damage.type:
            case DamageType.Physical:
                return self._reduced_physical_damage(amount, damage.target_id)
            case DamageType.Magic:
                return self._reduced_magic_damage(amount, damage.target_id)
        return amount
    
    def _round_amount(self, amount) -> int:
        # Rounds fractional damage probabilistically
        ceil = amount % 1 > random()
        return int(amount) + int(ceil)

    def _apply_for_unit(self, target_id, amount):
        health = self.world.get_component(target_id, Health)

        if not health:
            return 0
        
        before = health.value
        health.value -= amount
        
        return before - health.value
    
    def _check_death(self, target_id):
        health = self.world.get_component(target_id, Health)
        if health and health.value <= 0:
            return True
        return False