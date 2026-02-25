from system.system import System
from component.stats import Health, Mana, Stamina
from core.event import UseResourceEvent

class ResourceSystem(System):
    def __init__(self, world):
        super().__init__(world)
        self.regenerable = [
            Health,
            Mana,
            Stamina
        ]
    
    def update(self, delta):
        for meter_type in self.regenerable:
            self._update_meters(meter_type, delta)
    
    def use_resource(self, entity_id, resource):
        result = {}

        for resource_type in resource:
            resource_component = self.world.get_component(entity_id, resource_type)
            if resource_component:
                old_value = resource_component.value
                resource_component.value -= resource[resource_type]
                result[resource_type] = old_value - resource_component.value
        
        return UseResourceEvent(entity_id, result)

    def _update_meters(self, meter_type, delta):
        for unit_id in self.world.components[meter_type]:
            meter = self.world.get_component(unit_id, meter_type)
            self._update_meter(meter, delta)

    def _update_meter(self, meter, delta):
        meter.value += meter.effective_regen * delta