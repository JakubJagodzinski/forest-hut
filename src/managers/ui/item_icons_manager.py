import os

import pygame

from src.interface.interface_constants import INTERFACE_TILE_SIZE
from src.paths import PATH_IMAGE_EMPTY_ITEM_SLOT, DIR_ASSETS_ITEM_ICONS


class ItemIconsManager:
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

            self.empty_item_slot_icon = pygame.image.load(PATH_IMAGE_EMPTY_ITEM_SLOT).convert_alpha()
            self.empty_item_slot_icon = pygame.transform.scale(
                self.empty_item_slot_icon,
                (
                    INTERFACE_TILE_SIZE,
                    INTERFACE_TILE_SIZE
                )
            )

            self.item_icons = self.load_item_icons()

    @staticmethod
    def load_item_icons() -> dict:
        item_icons = {}
        item_icons_directories = os.listdir(DIR_ASSETS_ITEM_ICONS)
        for directory_name in item_icons_directories:
            icon_names = os.listdir(os.path.join(DIR_ASSETS_ITEM_ICONS, directory_name))
            for icon_name in icon_names:
                icon_path = os.path.join(DIR_ASSETS_ITEM_ICONS, directory_name, icon_name)
                item_icon = pygame.image.load(icon_path).convert_alpha()
                item_icon = pygame.transform.scale(item_icon, (INTERFACE_TILE_SIZE, INTERFACE_TILE_SIZE))
                item_icons[os.path.join(directory_name, icon_name)] = item_icon
        return item_icons

    def get_item_icon(self, icon_name):
        return self.item_icons.get(icon_name, self.empty_item_slot_icon)
