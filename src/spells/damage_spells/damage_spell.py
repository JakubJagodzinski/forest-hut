from src.spells.spell import Spell


class DamageSpell(Spell):

    def __init__(self, caster_reference, cast_time_in_seconds, cooldown_time_in_seconds, damage, spell_range):
        super().__init__(
            caster_reference=caster_reference,
            cast_time_in_seconds=cast_time_in_seconds,
            cooldown_time_in_seconds=cooldown_time_in_seconds
        )

        self._damage = damage
        self._spell_range = spell_range

    @property
    def damage(self):
        return self._damage

    @property
    def spell_range(self):
        return self._spell_range
