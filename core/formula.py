from component.attributes import Agility, Intelligence, Strength
from component.stats import Health, AttackSpeed
from core.statref import StatRef

class Formula:
    requires = []

    @staticmethod
    def calculate():
        raise NotImplementedError

class BaseArmorFormula(Formula):
    requires = [
        StatRef(Agility, "effective_value")
    ]

    @staticmethod
    def calculate(agility_effective_value):
        return agility_effective_value

class BaseMagicResistanceFormula(Formula):
    requires = [
        StatRef(Intelligence, "effective_value")
    ]

    @staticmethod
    def calculate(intelligence_effective_value):
        return 1 - (0.95 ** intelligence_effective_value)

class BaseMaxHealthFormula(Formula):
    requires = [
        StatRef(Strength, "effective_value")
    ]

    @staticmethod
    def calculate(strength_effective_value):
        return 100 + strength_effective_value

class BaseHealthRegenFormula(Formula):
    requires = [
        StatRef(Health, "effective_max_value"), 
        StatRef(Strength, "effective_value")
    ]

    @staticmethod
    def calculate(health_effective_max_value, strength_effective_value):
        return health_effective_max_value * 0.01 + strength_effective_value

class AttackDelayFormula():
    requires = [
        StatRef(AttackSpeed, "effective_value"), 
    ]

    @staticmethod
    def calculate(attack_speed_effective_value):
        return 1 / (attack_speed_effective_value * 0.1)