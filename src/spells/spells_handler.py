class SpellsHandler:

    def __init__(self, game_surface, caster, is_npc=True):
        self.game_surface = game_surface
        self.caster = caster
        self.is_npc = is_npc

        self.spells = []

    def load_spells(self):
        from src.database_service import DatabaseService

        if self.is_npc:
            character_spells = DatabaseService.get_npc_spells(self.caster.get_id())
        else:
            character_spells = DatabaseService.get_character_spells(self.caster.get_id())

        for spell in character_spells:
            pass

    def add_spell(self, spell):
        self.spells.append(spell)

    def draw_casting_animation(self):
        for spell in self.spells:
            if spell.is_being_casted():
                spell.draw_casting_animation()

    def handle_spell_cast_finish(self):
        for spell in self.spells:
            spell.handle_cast_finish()

    def cancel_spell_cast(self):
        for spell in self.spells:
            spell.cancel_cast()
