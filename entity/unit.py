class Stats:
    def __init__(self):
        self.max_health = 100
        self.health = 100

        self.armor = 30
        self.magic_resist = 0
        self.damage = 10

class Unit:
    def __init__(self, name):
        self.name = name
        self.alive = True

        self.stats = Stats()
        self.effects = []

    def hit(self, target):
        from entity.damage import Damage
        from entity.damage_type import PhysicalDamageType

        return Damage(self, target, PhysicalDamageType(), self.stats.damage)

    def log(self):
        print('--------')
        print(self.name)
        print(self.alive)
        print(f'{self.stats.health} / {self.stats.max_health}')
        print('--------')