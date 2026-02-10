from typing import Protocol
from entity.unit import Unit

class DamageType(Protocol):
    def reduce(self, value: float, target: Unit) -> float:
        pass

class PhysicalDamageType(DamageType):
    def reduce(self, value, target):
        ARMOR_COEFFICIENT = 95 / 100 # damage gains with 1 armor
        reduce_coefficient = ARMOR_COEFFICIENT ** target.stats.armor
        return value * reduce_coefficient

class MagicDamageType(DamageType):
    def reduce(self, value, target):
        reduce_coefficient = 1 - target.stats.magic_resist
        return value * reduce_coefficient

class PureDamageType(DamageType):
    def reduce(self, value, target):
        return value