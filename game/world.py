from engine.world import World

from game.system.combat import CombatSystem
from game.system.damage import DamageSystem
from game.system.cooldown import CooldownSystem
from game.system.ability import AbilitySystem
from game.system.resource import ResourceSystem
from game.system.stats.stats import StatsSystem
from game.system.attack_speed import AttackSpeedSystem
from game.system.effect import EffectSystem
from game.system.god import God

from game.builder.unit import UnitBuilder

class GameWorld(World):
    def __init__(self, game_config_path="config/game.json", logger=None):
        super().__init__()

        self.registry_system(CombatSystem(self))
        self.registry_system(DamageSystem(self, game_config_path))
        self.registry_system(CooldownSystem(self, game_config_path))
        self.registry_system(AbilitySystem(self))
        self.registry_system(ResourceSystem(self))
        self.registry_system(StatsSystem(self))
        self.registry_system(AttackSpeedSystem(self))
        self.registry_system(EffectSystem(self))

        self.unit_builder = UnitBuilder(self)

        # Temporary object
        self.god = God(self)

        self.logger = logger

    def update(self, delta):
        self.get_system(CooldownSystem).update(delta)
        self.get_system(ResourceSystem).update(delta)
        self.get_system(EffectSystem).update(delta)
        super().update(delta)