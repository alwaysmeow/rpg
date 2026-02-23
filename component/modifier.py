from typing import Dict, List
from collections import defaultdict

from core.modifier_type import ModifierType

class ModifierData:
    def __init__(self, stat: type, value: float = 0, type: ModifierType = ModifierType.Flat):
        self.stat = stat
        self.value = value
        self.type = type

class ModifierIndex:
    def __init__(self):
        self.map: Dict[type, List[int]] = defaultdict(list)

class SourceModifiers(ModifierIndex): pass
class TargetModifiers(ModifierIndex): pass