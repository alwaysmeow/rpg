from entity.damage import *
from entity.unit import *

class DamagePipeline:
    def __init__(self, damage):
        self.value = damage.amount
        self.damage = damage
        self.steps = [
            self.modifiers_step,
            self.resistance_step,
            self.apply_step,
        ]

    def execute(self):
        for step in self.steps:
            self.value = step()
    
    def modifiers_step(self):
        return self.value
    
    def resistance_step(self):
        return self.damage.type.reduce(self.value, self.damage.target)
    
    def apply_step(self):
        target = self.damage.target
        target.stats.health -= self.value
        
        if target.stats.health <= 0:
            target.stats.health = 0
            target.alive = False
        
        return self.value