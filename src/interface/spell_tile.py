from typing import override

from src.interface.interface_tile import InterfaceTile
from src.managers.ui.spell_icons_manager import SpellIconsManager


class SpellTile(InterfaceTile):
    spell_icons_manager = None

    def __init__(self, game_surface, icon_name, x, y):
        super().__init__(
            game_surface=game_surface,
            x=x,
            y=y
        )

        self.icon_name = icon_name

    @classmethod
    def setup_references(cls):
        cls.spell_icons_manager = SpellIconsManager

    @override
    def are_requirements_met(self):
        return True

    @override
    def is_empty(self):
        pass
