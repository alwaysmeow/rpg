from rich.text import Text

from component.name import Name
from component.stats import Armor, MagicResistance, Health
from component.ability import Cooldown
from component.tag import *

from shared.damage_type import DamageType
from shared.event_type import EventType
from shared.event_result import *

class Logger:
    def __init__(self, world, sink=print, markup=True):
        self.world = world
        self.sink = sink
        self.markup = markup

        subscribers = {
            EventType.ATTACK: self._log_attack_event_result,
            EventType.CAST_END: self._log_cast_event_result,
            EventType.DAMAGE: self._log_damage_event_result,
            EventType.DEATH: self._log_death_event_result,
        }

        for event_type in subscribers:
            self.world.events.subscribe(event_type, subscribers[event_type])
    
    def _write(self, markup_text):
        text = Text.from_markup(markup_text)
        self.sink(text if self.markup else text.plain)

    def log_unit(self, unit_id):
        self._write(f"\nName: {self._marked_name(unit_id)}")
        self._write(f"Health: {self.world.get_component(unit_id, Health).value} / {self.world.get_component(unit_id, Health).effective_max_value}")
        self._write(f"Armor: {self.world.get_component(unit_id, Armor).effective_value}")
        self._write(f"Magic Resist: {self.world.get_component(unit_id, MagicResistance).effective_value}\n")
    
    def log_combat(self, combat_id, teams):
        for team_index in range(len(teams)):
            self._write(f"\nTeam {team_index + 1}:")
            for unit_id in teams[team_index]:
                self.log_unit(unit_id)

    def log_ability(self, ability_id):
        self._write(f"\nID: {ability_id}")
        self._write(f"Cooldown: {self.world.get_component(ability_id, Cooldown).value} / {self.world.get_component(ability_id, Cooldown).effective_max_value}\n")
    
    def _log_attack_event_result(self, result: AttackEventResult):
        attacker_name = self._marked_name(result.attacker_id)
        target_name = self._marked_name(result.target_id)
        self._write(f"- {attacker_name} attacks {target_name}")

    def _log_cast_event_result(self, result: CastEventResult):
        attacker_name = self._marked_name(result.attacker_id)
        target_name = self._marked_name(result.target_id)
        self._write(f"- {attacker_name} casts spell on {target_name}")

    def _log_damage_event_result(self, result: DamageEventResult):
        source_name = self._marked_name(result.source_id)
        target_name = self._marked_name(result.target_id)
        damage_value = self._marked_damage(result.amount, result.damage_type)
        self._write(f"- {source_name} deals {damage_value} damage to {target_name}")

    def _log_death_event_result(self, result: DeathEventResult):
        killer_name = self._marked_name(result.killer_id)
        victim_name = self._marked_name(result.victim_id)
        self._write(f"- {killer_name} [red]killed[/red] {victim_name}")

    def error(self, text):
        self._write(f"- [bold red]ERROR:[/bold red] {text} - {self.world.time.now}")

    def log(self, text):
        self._write(f"\n- LOG: {text} - {self.world.time.now}\n")

    def _marked_name(self, entity_id):
        name_component = self.world.get_component(entity_id, Name)

        if name_component:
            name = name_component.name
        else:
            entity_type = "Entity"
            if self.world.has_tag(entity_id, Unit):
                entity_type = "Unit"
            elif self.world.has_tag(entity_id, Ability):
                entity_type = "Ability"
            elif self.world.has_tag(entity_id, Combat):
                entity_type = "Combat"

            name = f"{entity_type} {entity_id}"

        return f"[cyan]{name}[/cyan]"
    
    def _marked_damage(self, value, damage_type):
        return f"[{damage_type.color}]{value}[/{damage_type.color}]"