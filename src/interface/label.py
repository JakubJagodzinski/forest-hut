import pygame

from src.colors import BLACK, WHITE
from src.interface.interface_constants import BORDER_WIDTH


class Label:
    def __init__(self, game_surface, x, y, width, height, background_color=BLACK, border_color=WHITE, border_radius=90):
        self.game_surface = game_surface
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )
        self.background_color = background_color
        self.border_color = border_color
        self.border_radius = border_radius

    @property
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        # draw background
        pygame.draw.rect(
            self.game_surface,
            self.background_color,
            self.rect,
            border_radius=self.border_radius
        )

        # draw border
        pygame.draw.rect(
            self.game_surface,
            self.border_color,
            self.rect,
            width=BORDER_WIDTH,
            border_radius=self.border_radius
        )
