from component.attributes import Agility, Intelligence, Strength
from component.stats import Health

class Formula:
    requires = []

    @staticmethod
    def calculate():
        raise NotImplementedError

class BaseArmorFormula(Formula):
    requires = [Agility]

    @staticmethod
    def calculate(agility):
        return agility.effective_value

class BaseMagicResistFormula(Formula):
    requires = [Intelligence]

    @staticmethod
    def calculate(intelligence):
        return 1 - (0.95 ** intelligence.effective_value)

class BaseMaxHealthFormula(Formula):
    requires = [Strength]

    @staticmethod
    def calculate(strength):
        return 100 + strength.effective_value

class BaseHealthRegenFormula(Formula):
    requires = [Health, Strength] # TODO: fix circular dependency

    @staticmethod
    def calculate(health, strength):
        return health.effective_max_value * 0.01 + strength.effective_value