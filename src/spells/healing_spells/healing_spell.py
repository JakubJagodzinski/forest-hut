from src.spells.spell import Spell


class HealingSpell(Spell):

    def __init__(self, caster_reference, cast_time_in_seconds, cooldown_time_in_seconds, health_points):
        super().__init__(
            caster_reference=caster_reference,
            cast_time_in_seconds=cast_time_in_seconds,
            cooldown_time_in_seconds=cooldown_time_in_seconds
        )

        self.health_points = health_points

    def get_health_points(self):
        return self.health_points
