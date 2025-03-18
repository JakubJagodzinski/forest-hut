from abc import abstractmethod
from typing import override

import pygame

from src.colors import WHITE, BLACK
from src.entities.entity import Entity
from src.fonts import FONT_ARIAL_18
from src.interface.interface_constants import BORDER_WIDTH
from src.managers.core.mouse_manager import MouseManager
from src.sprites.object_sprite import ObjectSprite


class Object(Entity):
    NAME_FONT = FONT_ARIAL_18
    NAME_OFFSET_Y = 20
    NAME_TEXT_PADDING_X = 5

    def __init__(self, game_surface, map_id, x, y, draw_size, name, sprite_name=None):
        super().__init__(game_surface, map_id, x, y, draw_size, name)

        self.black_name_text = self.NAME_FONT.render(name, True, BLACK)
        self.white_name_text = self.NAME_FONT.render(name, True, WHITE)
        self.name_rect = pygame.Rect(
            x,
            y - self.NAME_OFFSET_Y,
            self.black_name_text.get_width() + (2 * self.NAME_TEXT_PADDING_X),
            self.black_name_text.get_height()
        )

        if sprite_name is not None:
            self.animated_sprite = ObjectSprite(self.game_surface, sprite_name, self._draw_size)

        self.is_active = True

    def is_name_hovered(self) -> bool:
        return self.name_rect.collidepoint(pygame.mouse.get_pos())

    @abstractmethod
    def interact(self):
        pass

    @override
    @property
    def is_clicked(self):
        return MouseManager.is_left_clicked() and self.is_name_hovered()

    def draw_name(self, screen_position):
        screen_x, screen_y = screen_position

        self.name_rect.x = screen_x - (self.name_rect.width // 2)
        self.name_rect.y = (screen_y
                            - (self._draw_size // 2)
                            - self.NAME_OFFSET_Y)

        if self.is_name_hovered():
            background_color = BLACK
            border_color = WHITE
            text = self.white_name_text
        else:
            background_color = WHITE
            border_color = BLACK
            text = self.black_name_text

        # draw white background
        pygame.draw.rect(
            self.game_surface,
            background_color,
            self.name_rect,
            border_radius=90
        )

        # draw black border
        pygame.draw.rect(
            self.game_surface,
            border_color,
            self.name_rect,
            width=BORDER_WIDTH,
            border_radius=90
        )

        self.game_surface.blit(text, (self.name_rect.x + self.NAME_TEXT_PADDING_X, self.name_rect.y))

    @override
    def draw(self):
        super().draw()
        if self.map_manager.map_id == self._map_id:
            position_on_screen = self.map_manager.convert_map_position_to_screen_position(self.x, self.y)
            self.draw_name(position_on_screen)
