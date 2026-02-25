from dataclasses import dataclass
from typing import Dict

from component.meter import Meter

class AbilityEffect:
    def __init__(self, handler = lambda world, caster, target: None):
        self.handler = handler

@dataclass
class Owner:
    unit_id: int = None

@dataclass
class CastTime:
    value: int = 0

@dataclass
class ResourceCost:
    cost: Dict[type, int]

class Cooldown(Meter): 
    # value = 1 - ability is ready
    pass