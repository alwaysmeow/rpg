from queue import Queue

from component.stats import Health
from component.tag import Dead
from entity.damage_type import DamageType

class Damage:
    def __init__(self, source, target, type: DamageType, amount: int):
        self.source = source
        self.target = target
        self.type = type
        self.amount = amount

class DamageSystem:
    def __init__(self, world):
        self.world = world
        self._damage_queue = Queue()
    
    def queue_damage(self, source_id, target_id, damage_type, base_amount):
        self._damage_queue.append(Damage(source_id, target_id, damage_type, base_amount))
    
    def process_damage_queue(self):
        while self._damage_queue:
            damage = self._damage_queue.get()
            self._process_damage(damage)
    
    def _process_damage(self, damage):
        amount = damage.amount

        amount = self._apply_modifiers(damage, amount)
        amount = self._apply_resistance(damage, amount)
        amount = self._apply_for_unit(damage.target_id, amount)

        if self._check_death(damage.target_id):
            self._on_death(damage.target_id)
        else:
            self._on_damage(damage.target_id, amount)

    def _apply_modifiers(self, damage, amount):
        # TODO: modifiers processing
        return amount
    
    def _apply_resistance(self, damage, amount):
        # TODO: resistance processing
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
            self.world.add_tag(target_id, Dead)
            return True
        return False
    
    def _on_death(self, target_id):
        # TODO: events triggered by death
        pass

    def _on_damage(self, target_id, amount):
        # TODO: events triggered by damage
        pass