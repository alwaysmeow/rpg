from component.health import Health

class UnitSystem:
    def __init__(self, world):
        self.world = world

    def create_unit(self):
        unit_id = self.world.create_entity()

        self.world.add_component(unit_id, Health, 100, 0)

        return unit_id