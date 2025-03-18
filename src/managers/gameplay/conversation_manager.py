import os
from typing import override

import pygame

from src.colors import WHITE
from src.common_utils import remove_filename_extension
from src.interface.interface_constants import BORDER_WIDTH, LOWER_UI_BAR_HEIGHT, XP_BAR_HEIGHT, WINDOW_DEFAULT_STRIPE_HEIGHT
from src.interface.window import Window
from src.paths import DIR_ASSETS_PORTRAITS


class ConversationManager(Window):
    _instance = None

    WIDTH = 800
    HEIGHT = 200

    WINDOW_OFFSET = 5
    PORTRAIT_OFFSET = 5

    _portraits = {}

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_surface):
        x = (game_surface.get_width() // 2) - (self.WIDTH // 2)
        y = (game_surface.get_height()
             - LOWER_UI_BAR_HEIGHT
             - XP_BAR_HEIGHT
             - self.HEIGHT
             - self.WINDOW_OFFSET)
        super().__init__(game_surface, x, y, self.WIDTH, self.HEIGHT)
        self.load_portraits()
        self.portrait_name = ''
        # self.open('cultist', 'cultist')

    @classmethod
    def load_portraits(cls):
        portraits_names = os.listdir(DIR_ASSETS_PORTRAITS)
        for portrait_name in portraits_names:
            portrait_image = pygame.image.load(os.path.join(DIR_ASSETS_PORTRAITS, portrait_name)).convert_alpha()
            portrait_image = pygame.transform.scale(
                portrait_image,
                (
                    cls.HEIGHT - (2 * WINDOW_DEFAULT_STRIPE_HEIGHT) - (2 * cls.PORTRAIT_OFFSET),
                    cls.HEIGHT - (2 * WINDOW_DEFAULT_STRIPE_HEIGHT) - (2 * cls.PORTRAIT_OFFSET)
                )
            )
            cls._portraits[remove_filename_extension(portrait_name)] = portrait_image

    @override
    def open(self, npc_name, portrait_name):
        self.set_name(npc_name)
        self.portrait_name = portrait_name
        super().open()

    def draw(self):
        if self.is_open:
            super().draw()
            self.game_surface.blit(self._portraits[self.portrait_name], (self.content_rect.x, self.content_rect.y))
            pygame.draw.rect(
                self.game_surface,
                WHITE,
                pygame.Rect(
                    self.content_rect.x + self.PORTRAIT_OFFSET,
                    self.content_rect.y + self.PORTRAIT_OFFSET,
                    self.content_rect.height - (2 * self.PORTRAIT_OFFSET),
                    self.content_rect.height - (2 * self.PORTRAIT_OFFSET)
                ),
                width=BORDER_WIDTH
            )
