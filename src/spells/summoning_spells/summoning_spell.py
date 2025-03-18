from src.spells.spell import Spell


class SummoningSpell(Spell):

    def __init__(self, caster_reference, cast_time_in_seconds, cooldown_time_in_seconds):
        super().__init__(
            caster_reference=caster_reference,
            cast_time_in_seconds=cast_time_in_seconds,
            cooldown_time_in_seconds=cooldown_time_in_seconds
        )