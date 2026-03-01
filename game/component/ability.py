from dataclasses import dataclass
from typing import Dict

from game.component.meter import Meter

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