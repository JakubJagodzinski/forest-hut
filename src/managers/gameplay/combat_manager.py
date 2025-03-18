class CombatManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            self.map_manager = None
            self.npcs_manager = None

            self.spell_queue = []

    def setup_references(self):
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.gameplay.npcs_manager import NpcsManager

        self.map_manager = MapManager.get_instance()
        self.npcs_manager = NpcsManager.get_instance()

    def add_spell_to_queue(self, spell):
        self.spell_queue.append(spell)

    def get_targets_for_spell(self, spell):
        caster_position = spell.caster_reference.position
        all_targets = self.npcs_manager.get_npcs_in_range(caster_position, spell.get_range())
        valid_targets = [target for target in all_targets if spell.caster_reference.is_enemy(target)]
        return valid_targets

    def process_spells(self):
        for spell in self.spell_queue:
            affected_targets = self.get_targets_for_spell(spell)
            for target in affected_targets:
                spell.apply_effect(target)
        self.spell_queue.clear()
