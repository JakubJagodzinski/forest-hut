import os

import pygame

from src.common_utils import remove_filename_extension
from src.enums.cursor_type import CursorType
from src.paths import DIR_ASSETS_CURSORS


class MouseManager:
    _instance = None

    CURSOR_SIZE = 50

    MOUSE_BUTTON_LEFT = 0
    MOUSE_BUTTON_MIDDLE = 1
    MOUSE_BUTTON_RIGHT = 2
    MOUSE_SCROLL_UP = 4
    MOUSE_SCROLL_DOWN = 5

    @classmethod
    def get_instance(cls):
        return cls._instance

    @classmethod
    def is_scrolled_up(cls, event):
        return event.button == cls.MOUSE_SCROLL_UP

    @classmethod
    def is_scrolled_down(cls, event):
        return event.button == cls.MOUSE_SCROLL_DOWN

    @classmethod
    def is_left_clicked(cls):
        return pygame.mouse.get_pressed()[cls.MOUSE_BUTTON_LEFT]

    @classmethod
    def is_right_clicked(cls):
        return pygame.mouse.get_pressed()[cls.MOUSE_BUTTON_RIGHT]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_surface):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.game_surface = game_surface
            self._cursors = {}
            self._load_cursors()
            self._cursor_rect = self._cursors[CursorType.POINT].get_rect()
            self._hotspot = (self._cursor_rect.width // 2, self._cursor_rect.height)
            pygame.mouse.set_visible(False)

    def _load_cursors(self) -> None:
        cursors_names = os.listdir(DIR_ASSETS_CURSORS)
        for cursor_name in cursors_names:
            cursor = pygame.image.load(os.path.join(DIR_ASSETS_CURSORS, cursor_name)).convert_alpha()
            cursor = pygame.transform.scale(cursor, (self.CURSOR_SIZE, self.CURSOR_SIZE))
            self._cursors[remove_filename_extension(cursor_name)] = cursor

    def draw_cursor(self, cursor_name) -> None:
        cursor_name = self._cursors[cursor_name] if cursor_name in self._cursors else self._cursors[CursorType.POINT]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._cursor_rect.topleft = (mouse_x - self._hotspot[0], mouse_y)
        self.game_surface.blit(cursor_name, self._cursor_rect)
