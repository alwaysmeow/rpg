from typing import Protocol
from component.attributes import Agility, Intelligence, Strength
from component.stats import Health

class Formula(Protocol):
    def calculate(self, world, entity_id):
        pass

class BaseArmorFormula(Formula):
    def calculate(self, world, entity_id):
        agility = world.get_component(entity_id, Agility)
        return agility

class BaseMagicResistFormula(Formula):
    def calculate(self, world, entity_id):
        intelligence = world.get_component(entity_id, Intelligence)
        return 1 - (0.95 ** intelligence)

class BaseMaxHealthFormula(Formula):
    def calculate(self, world, entity_id):
        strength = world.get_component(entity_id, Strength)
        return 100 + strength

class BaseHealthRegenFormula(Formula):
    def calculate(self, world, entity_id):
        max_health = world.get_component(entity_id, Health).effective_max_value
        strength = world.get_component(entity_id, Strength)
        return max_health * 0.01 + strength