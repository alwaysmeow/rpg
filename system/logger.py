from rich.console import Console

from component.name import Name
from component.stats import Armor, MagicResist, Health
from component.ability import Cooldown

from system.event import AttackEventResult, CastEventResult, CombatEventResult, CooldownEventResult, DeathEventResult, DamageEventResult

class Logger:
    def __init__(self, world):
        self.world = world

        self.console = Console()
    
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
        self.console.print(f"- [cyan]{source_name}[/cyan] deals [red]{result.amount}[/red] {result.damage_type._value_} damage to [cyan]{target_name}[/cyan]")

    def _log_death_event_result(self, result: DeathEventResult):
        killer_name = self._get_unit_name(result.killer_id)
        victim_name = self._get_unit_name(result.victim_id)
        self.console.print(f"- [cyan]{killer_name}[/cyan] [red]killed[/red] [cyan]{victim_name}[/cyan]")

    def error(self, text):
        self.console.print(f"- [bold red]ERROR:[/bold red] {text} - {self.world.time.now}")

    def log(self, text):
        print(f"\n- LOG: {text} - {self.world.time.now}\n")
    
    def _get_unit_name(self, unit_id):
        name_component = self.world.get_component(unit_id, Name)
        return name_component.name if name_component else f"Unit {unit_id}"