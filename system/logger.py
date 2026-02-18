from component.name import Name
from component.stats import Armor, MagicResist, Health
from component.ability import Cooldown

from system.event import AttackEventResult, CastEventResult, CombatEventResult, CooldownEventResult, DeathEventResult, DamageEventResult

class Logger:
    def __init__(self, world):
        self.world = world
    
    def log_unit(self, unit_id):
        print(f"\nName: {self.world.get_component(unit_id, Name).name}")
        print(f"Health: {self.world.get_component(unit_id, Health).value} / {self.world.get_component(unit_id, Health).effective_max_value}")
        print(f"Armor: {self.world.get_component(unit_id, Armor).effective_value}")
        print(f"Magic Resist: {self.world.get_component(unit_id, MagicResist).effective_value}")
    
    def log_combat(self, combat_id, teams):
        for team_index in range(len(teams)):
            print(f"\nTeam {team_index + 1}:")
            for unit_id in teams[team_index]:
                self.log_unit(unit_id)

    def log_ability(self, ability_id):
        print(f"\nID: {ability_id}")
        print(f"Cooldown: {self.world.get_component(ability_id, Cooldown).value} / {self.world.get_component(ability_id, Cooldown).effective_max_value}")

    def log_event_result(self, result):
        match result:
            case DamageEventResult():
                self._log_damage_event_result(result)
            case DeathEventResult():
                self._log_death_event_result(result)
    
    def _log_damage_event_result(self, result: DamageEventResult):
        source_name = self._get_unit_name(result.source_id)
        target_name = self._get_unit_name(result.target_id)
        print(f"- {source_name} deals {result.amount} {result.damage_type._value_} damage to {target_name}")

    def _log_death_event_result(self, result: DeathEventResult):
        killer_name = self._get_unit_name(result.killer_id)
        victim_name = self._get_unit_name(result.victim_id)
        print(f"- {killer_name} killed {victim_name}")

    def error(self, text):
        print(f"\n- ERROR: {text} - {self.world.time.now}\n")

    def log(self, text):
        print(f"\n- LOG: {text} - {self.world.time.now}\n")
    
    def _get_unit_name(self, unit_id):
        name_component = self.world.get_component(unit_id, Name)
        return name_component.name if name_component else f"Unit {unit_id}"