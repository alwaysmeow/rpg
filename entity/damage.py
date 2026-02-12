from entity.damage_type import DamageType

class Damage:
    def __init__(self, source, target, type: DamageType, amount: int):
        self.source = source
        self.target = target
        self.type = type
        self.amount = amount