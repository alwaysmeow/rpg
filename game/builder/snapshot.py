import json

from game.core.snapshot import Snapshot

def is_json_serializable(value):
    try:
        json.dumps(value)
        return True
    except (TypeError, OverflowError):
        return False

class SnapshotBuilder:
    def build(world):
        snapshot = Snapshot(world.now())

        entities = {}

        for entity_id in world.entities:
            entities[entity_id] = {}
            entities[entity_id]["Tags"] = []
        
        for tag_type in world.tags:
            tag_name = str(tag_type.__name__)
            for entity_id in world.tags[tag_type]:
                entities[entity_id]["Tags"].append(tag_name)

        for component_type in world.components:
            component_name = str(component_type.__name__)
            for entity_id in world.components[component_type]:
                component = world.components[component_type][entity_id]
                component_dict = component.__dict__

                snapshot_item = {}

                for key in component_dict:
                    value = component_dict[key]

                    # Behaviours, Formulas, Stats are not in snapshot
                    if is_json_serializable(value):
                        snapshot_item[key] = value

                entities[entity_id][component_name] = snapshot_item

        snapshot.entities = entities

        return snapshot