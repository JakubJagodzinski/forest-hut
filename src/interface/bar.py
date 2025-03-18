import pygame

from src.colors import BLACK, WHITE
from src.fonts import FONT_ARIAL_18
from src.interface.interface_constants import BORDER_WIDTH


class Bar:
    INFO_RECT_WIDTH_PADDING = 5

    def __init__(self, game_surface, x, y, width, height, color, is_fill_complement=False, parts=1, text=None,
                 border_radius=0):
        self.game_surface = game_surface
        self.width = width
        self.height = height
        self.color = color
        self.is_fill_complement = is_fill_complement
        self.parts = parts
        self.border_radius = border_radius
        self.rect = pygame.Rect(
            x,
            y,
            self.width,
            self.height
        )
        self.text = text
        self.hoverable = text is not None
        self.info_text_font = FONT_ARIAL_18

    def set_position(self, x, y):
        self.rect = pygame.Rect(
            x,
            y,
            self.width,
            self.height
        )

    def draw(self, value: int, max_value: int) -> None:
        pygame.draw.rect(
            self.game_surface,
            BLACK,
            self.rect,
            border_radius=self.border_radius
        )

        # draw filling
        if self.is_fill_complement:
            filled_width = int(((max_value - value) / max_value) * self.width)
        else:
            filled_width = int((value / max_value) * self.width)
        pygame.draw.rect(
            self.game_surface,
            self.color,
            (
                self.rect.x + BORDER_WIDTH,
                self.rect.y + BORDER_WIDTH,
                filled_width - (2 * BORDER_WIDTH),
                self.height - (2 * BORDER_WIDTH)
            ),
            border_radius=self.border_radius
        )

        # draw parts
        part_width = (self.width // self.parts)
        for part_nr in range(1, self.parts):
            division_x = (part_nr * part_width + ((part_nr - 1) * BORDER_WIDTH))
            pygame.draw.rect(
                self.game_surface,
                BLACK,
                (
                    self.rect.x + division_x - BORDER_WIDTH,
                    self.rect.y,
                    BORDER_WIDTH,
                    self.height
                )
            )

    def draw_info(self, value, max_value):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        info_rect_x = mouse_x + 20
        info_rect_y = mouse_y
        info_text = self.info_text_font.render(
            f'{self.text}: {value}/{max_value} ({round(value / max_value * 100, 2)}%)',
            True,
            WHITE
        )
        info_rect_height = info_text.get_height()
        info_rect_width = info_text.get_width() + (2 * Bar.INFO_RECT_WIDTH_PADDING)
        info_rect = pygame.Rect(info_rect_x, info_rect_y, info_rect_width, info_rect_height)
        # draw black background
        pygame.draw.rect(
            self.game_surface,
            BLACK,
            info_rect,
            border_radius=45
        )

        # draw white border
        pygame.draw.rect(
            self.game_surface,
            WHITE,
            info_rect,
            width=BORDER_WIDTH,
            border_radius=45
        )

        self.game_surface.blit(info_text, (info_rect_x + Bar.INFO_RECT_WIDTH_PADDING, info_rect_y))

    @property
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw_hovered(self, value: int, max_value: int):
        if self.hoverable and self.is_hovered:
            self.draw_info(value, max_value)
