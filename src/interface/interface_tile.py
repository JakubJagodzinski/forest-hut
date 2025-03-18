from abc import abstractmethod

import pygame

from src.colors import RED, WHITE, BLACK
from src.fonts import FONT_ALICE_IN_WONDERLAND_32
from src.interface.interface_constants import INTERFACE_TILE_SIZE, BORDER_WIDTH
from src.managers.core.mouse_manager import MouseManager


class InterfaceTile:
    REQUIREMENTS_NOT_MET_OVERLAY = (pygame.Surface((INTERFACE_TILE_SIZE, INTERFACE_TILE_SIZE), pygame.SRCALPHA))
    REQUIREMENTS_NOT_MET_OVERLAY.fill(RED + (90,))

    NAME_FONT = FONT_ALICE_IN_WONDERLAND_32

    EMPTY_INTERFACE_TILE_NAME = 'empty'
    EMPTY_INTERFACE_TILE_NAME_TEXT = NAME_FONT.render(EMPTY_INTERFACE_TILE_NAME, True, WHITE)

    def __init__(self, game_surface, x, y):
        self.game_surface = game_surface
        self.rect = pygame.Rect(
            x,
            y,
            INTERFACE_TILE_SIZE,
            INTERFACE_TILE_SIZE
        )

        self.icon = None

        self.name = self.EMPTY_INTERFACE_TILE_NAME
        self.name_text = self.NAME_FONT.render(self.name, True, WHITE)

    @abstractmethod
    def is_empty(self):
        pass

    @property
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_left_clicked(self):
        return MouseManager.is_left_clicked() and self.is_hovered

    def is_right_clicked(self):
        return MouseManager.is_right_clicked() and self.is_hovered

    @abstractmethod
    def are_requirements_met(self):
        pass

    def set_name(self, name):
        self.name = name
        self.name_text = self.NAME_FONT.render(self.name, True, WHITE)

    def draw_requirements_not_met_overlay(self):
        self.game_surface.blit(self.REQUIREMENTS_NOT_MET_OVERLAY, self.rect.topleft)

    def draw_icon(self):
        self.game_surface.blit(
            self.icon,
            self.rect
        )

        if not self.are_requirements_met():
            self.draw_requirements_not_met_overlay()

        # draw black border
        pygame.draw.rect(
            self.game_surface,
            BLACK,
            self.rect,
            width=BORDER_WIDTH
        )

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def draw_hover_info(self):
        pass

    def draw_hovered(self):
        if self.is_hovered:
            self.draw_hover_info()
