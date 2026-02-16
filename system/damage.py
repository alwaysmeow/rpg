from enum import Enum

from config_loader import load_config
from component.stats import Health, MagicResist, Armor
from component.tag import Dead
from system.event import EventType

class DamageType(Enum):
    Pure = 0
    Physical = 1
    Magic = 2

class Damage:
    def __init__(self, source_id, target_id, type: DamageType, amount: int):
        self.source_id = source_id
        self.target_id = target_id
        self.type = type
        self.amount = amount

class DamageSystem:
    def __init__(self, world):
        self.world = world

        config = load_config("config/game.json") # TODO: variable path
        self.armor_coefficient = config["armor_coefficient"]
    
    def queue_damage(self, source_id, target_id, damage_type, base_amount):
        """Напрямую планируем обработку урона"""
        damage = Damage(source_id, target_id, damage_type, base_amount)
        
        self.world.events.schedule(
            self.world.time.now,
            lambda d=damage: self._process_damage(d),
            EventType.DAMAGE,
            {
                "source_id": source_id,
                "target_id": target_id,
                "damage_type": damage_type,
            }
        )
    
    def _process_damage(self, damage):
        health = self.world.get_component(damage.target_id, Health)
        if not health:
            self.world.logger.error("Target has no health. Damage processing cancelled.")
            return 0
         
        amount = damage.amount

        amount = self._apply_modifiers(damage, amount)
        amount = self._apply_resistance(damage, amount)
        amount = self._apply_for_unit(damage.target_id, amount)

        if self._check_death(damage.target_id):
            self.world.events.schedule(
                self.world.time.now,
                self._create_death_handler(damage.target_id),
                EventType.DEATH,
                {
                    "unit_id": damage.target_id,
                }
            )
        
        return amount

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
        magic_resist = self.world.get_component(target_id, MagicResist)

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
    
    def _create_death_handler(self, unit_id):
        def death_handler():
            self.world.add_tag(unit_id, Dead)
            return unit_id

        return death_handler