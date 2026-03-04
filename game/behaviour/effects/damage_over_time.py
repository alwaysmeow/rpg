from game.component.behaviour import Behaviour
from game.component.effect import EffectTarget
from game.core.command import DamageCommand, EffectTickCommand

class DamageOverTimeBehaviour(Behaviour):
    def __init__(self, damage_type, damage_amount, delay):
        self.damage_type = damage_type
        self.damage_amount = damage_amount
        self.delay = delay

    def on_apply(self, world, effect_id):
        world.schedule(EffectTickCommand(effect_id))
    
    def on_tick(self, world, effect_id):
        from game.system.effect import EffectSystem
        effect_system = world.get_system(EffectSystem)
        
        target_id = None

        target = world.get_component(effect_id, EffectTarget)
        if target:
            target_id = target.entity_id

        world.schedule(
            DamageCommand(
                effect_id, 
                target_id, 
                self.damage_type, 
                self.damage_amount
            )
        )

        if effect_system.effect_still_active(effect_id):
            world.schedule(EffectTickCommand(effect_id), self.delay)
    
    def on_remove(self, world, effect_id):
        from game.system.effect import EffectSystem
        effect_system = world.get_system(EffectSystem)
        effect_system.cancel_unique_command((EffectTickCommand, effect_id))