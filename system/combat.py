from component.tag import Combat, Dead
from component.target import Target
from component.combat import CombatParticipation, CombatState

from system.event import DeathEventResult

from entity.event_type import EventType

class CombatSystem:
    def __init__(self, world):
        self.world = world

        self.world.events.subscribe(EventType.DEATH, self._update_targets)
    
    def create_combat(self, teams):
        combat_id = self.world.create_entity()

        self.world.add_component(combat_id, CombatState())

        for team_index in range(teams):
            for unit_id in teams[team_index]:
                self.world.add_component(unit_id, CombatParticipation(combat_id, team_index))

        self.world.add_tag(combat_id, Combat)

        return combat_id
    
    def _find_new_target(self, enemies):
        for enemy_id in enemies:
            if not self.world.has_tag(enemy_id, Dead):
                return enemy_id
        return None
    
    def _update_targets(self, death_event_result: DeathEventResult):
        victim_participation = self.world.get_component(death_event_result.unit_id, CombatParticipation)

        if victim_participation:
            teams = self._get_teams(victim_participation.combat_id)

            for team_index in range(len(teams)):
                if team_index != victim_participation.team_index:
                    enemies = self._get_enemies(teams, team_index)
                    new_target_id = self._find_new_target(enemies)
                    for unit_id in teams[team_index]:
                        self.world.add_component(unit_id, Target(new_target_id))
    
    def _get_teams(self, combat_id):
        # TODO: maybe create component for teams
        units_id = self.world.query_by_component(
            CombatParticipation,
            include_filters = {
                "combat_id": combat_id,
            },
        )

        teams = []

        for unit_id in units_id:
            participation = self.world.get_component(unit_id, CombatParticipation)
            while participation.team_index >= len(teams):
                teams.append([])
            teams[participation.team_index].append(unit_id)
        
        return teams

    def _get_enemies(self, teams, team_index):
        return [enemy for i, team in enumerate(teams) if i != team_index for enemy in team]
