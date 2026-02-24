from system.system import System
from component.stats import Health, Mana

class RegenerationSystem(System):
    def __init__(self, world):
        super().__init__(world)
        self.regenerable = [
            Health,
            Mana
        ]
    
    def update(self, delta):
        for meter_type in self.regenerable:
            self._update_meters(meter_type, delta)

    def _update_meters(self, meter_type, delta):
        for unit_id in self.world.components[meter_type]:
            meter = self.world.get_component(unit_id, meter_type)
            self._update_meter(meter, delta)

    def _update_meter(self, meter, delta):
        meter.value += meter.effective_regen * delta