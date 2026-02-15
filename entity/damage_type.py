# Legacy

from typing import Protocol

class DamageType(Protocol):
    def reduce(self, value: float, target) -> float:
        pass

class PhysicalDamageType(DamageType):
    def reduce(self, value: float, target) -> float:
        ARMOR_COEFFICIENT = 95 / 100 # damage gains with 1 armor
        reduce_coefficient = ARMOR_COEFFICIENT ** target.stats.armor
        return value * reduce_coefficient

class MagicDamageType(DamageType):
    def reduce(self, value: float, target) -> float:
        reduce_coefficient = 1 - target.stats.magic_resist
        return value * reduce_coefficient

class PureDamageType(DamageType):
    def reduce(self, value: float, target) -> float:
        return value