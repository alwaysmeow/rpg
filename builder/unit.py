"""
UnitBuilder — создаёт юнитов из JSON-конфигов.

Пример JSON-файла: см. units/warrior.json
"""

import json
from typing import Any

from system.event.event import EventSystem
from system.time import TimeSystem

from component.stats import (
    Health, Mana, Stamina,
    Armor, MagicResistance,
    AttackDamage, AttackSpeed
)

from component.attributes import Strength, Agility, Intelligence, Wisdom, Luck
from component.name import Name

from core.command import StatsCreateCommand

from tag.tag import Unit

class UnitBuilder:
    STAT_MAP: dict[str, type] = {
        "health":            Health,
        "mana":              Mana,
        "stamina":           Stamina,

        "armor":             Armor,
        "magic_resistance":  MagicResistance,
        "attack_damage":     AttackDamage,
        "attack_speed":      AttackSpeed,

        "strength":          Strength,
        "agility":           Agility,
        "intelligence":      Intelligence,
        "wisdom":            Wisdom,
        "luck":              Luck,
    }

    METER_TYPES = {Health, Mana, Stamina}
    
    def __init__(self, world):
        self.world = world

    def build_from_file(self, path: str) -> int:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.build_from_dict(data)

    def build_from_dict(self, data: dict) -> int:
        unit_id = self.world.create_entity()
        self.world.add_tag(unit_id, Unit)

        name = data.get("name", "Unknown")
        self.world.add_component(unit_id, Name(name))

        stats_data: dict = data.get("stats", {})
        components = []

        for key, params in stats_data.items():
            component = self._build_component(key, params)
            components.append(component)

        if components:
            self._exec_cmd(StatsCreateCommand(unit_id, components))

        return unit_id
    
    def _build_component(self, stat_key: str, params: Any):
        stat_type = self.STAT_MAP.get(stat_key)

        if isinstance(params, (int, float)):
            return stat_type(value=params, hardcoded=True)
        
        hardcoded = "value" in params

        return stat_type(**params, hardcoded=hardcoded)

    def _exec_cmd(self, command):
        self.world.get_system(EventSystem).scheduler.schedule(
            self.world.get_system(TimeSystem).now,
            command,
        )