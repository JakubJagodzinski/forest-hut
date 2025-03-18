import os

import pygame

from src.interface.interface_constants import INTERFACE_TILE_SIZE
from src.paths import PATH_IMAGE_EMPTY_SPELL_SLOT, DIR_ASSETS_SPELL_ICONS


class SpellIconsManager:
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

            self.empty_spell_slot_icon = pygame.image.load(PATH_IMAGE_EMPTY_SPELL_SLOT).convert_alpha()
            self.empty_spell_slot_icon = pygame.transform.scale(
                self.empty_spell_slot_icon,
                (
                    INTERFACE_TILE_SIZE,
                    INTERFACE_TILE_SIZE
                )
            )

            self.spell_icons = self.load_spell_icons()

    @staticmethod
    def load_spell_icons() -> dict:
        spell_icons = {}
        spell_icons_directories = os.listdir(DIR_ASSETS_SPELL_ICONS)
        for directory_name in spell_icons_directories:
            icon_names = os.listdir(os.path.join(DIR_ASSETS_SPELL_ICONS, directory_name))
            for icon_name in icon_names:
                icon_path = os.path.join(DIR_ASSETS_SPELL_ICONS, directory_name, icon_name)
                spell_icon = pygame.image.load(icon_path).convert_alpha()
                spell_icon = pygame.transform.scale(spell_icon, (INTERFACE_TILE_SIZE, INTERFACE_TILE_SIZE))
                spell_icons[os.path.join(directory_name, icon_name)] = spell_icon
        return spell_icons

    def get_spell_icon(self, icon_name):
        return self.spell_icons.get(icon_name, self.empty_spell_slot_icon)
