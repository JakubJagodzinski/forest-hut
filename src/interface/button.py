import pygame

from src.colors import WHITE, GRAY, BLACK
from src.common_utils import adjust_color
from src.fonts import FONT_ALICE_IN_WONDERLAND_32
from src.interface.interface_constants import BORDER_WIDTH
from src.managers.core.mouse_manager import MouseManager


class Button:
    BUTTON_TEXT_PADDING_X = 10
    BUTTON_TEXT_PADDING_Y = 5

    def __init__(
            self,
            game_surface,
            center_x,
            center_y,
            action,
            image=None,
            width=0,
            height=0,
            text=None,
            text_color=WHITE,
            font=FONT_ALICE_IN_WONDERLAND_32,
            button_color=GRAY,
            with_border=False,
            is_ready_check=None
    ):
        self._parent = game_surface
        self._action = action
        self._image = image
        self.font = font
        self._text_rect = None
        self._width = width
        self._height = height
        self._text = None
        if image is not None:
            self._width = self._image.get_width()
            self._height = self._image.get_width()

        self.x = center_x - (self._width // 2)
        self.y = center_y - (self._height // 2)

        if text is not None:
            self._text = font.render(text, False, text_color)
            if width == 0 or height == 0:
                self._width = self._text.get_width() + (2 * self.BUTTON_TEXT_PADDING_X)
                self._height = self._text.get_height() + (2 * self.BUTTON_TEXT_PADDING_Y)
            self.x = center_x - (self._width // 2)
            self.y = center_y - (self._height // 2)
            self._text_rect = self._text.get_rect(
                center=(self.x + (self._width // 2), self.y + (self._height // 2))
            )

        self._rect = pygame.Rect(self.x, self.y, self._width, self._height)

        self._is_pressed = False
        self._button_color = button_color
        self._button_hover_color = adjust_color(self._button_color, 1.4)
        self._button_press_color = adjust_color(self._button_color, 0.4)
        self._has_border = with_border
        self._is_active = True

        self._is_ready_check = is_ready_check

        self.not_ready_overlay_surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        self.not_ready_overlay_surface.fill((0, 0, 0, 0))
        overlay_color = (*BLACK, 127)
        pygame.draw.rect(
            self.not_ready_overlay_surface,
            overlay_color,
            (
                0,
                0,
                self._width,
                self._height
            ),
            border_radius=90
        )

    @property
    def is_hovered(self) -> bool:
        return self._rect.collidepoint(pygame.mouse.get_pos())

    @property
    def is_clicked(self) -> bool:
        return self._is_active and MouseManager.is_left_clicked() and self.is_hovered

    def handle_event(self) -> bool:
        if self._is_active and self.is_clicked:
            self._action()
            return True
        return False

    def draw_not_ready_overlay(self):
        self._parent.blit(self.not_ready_overlay_surface, (self.x, self.y))

    def draw(self) -> None:
        current_color = self._button_color
        if self.is_hovered:
            current_color = self._button_hover_color
        if self._is_pressed:
            current_color = self._button_press_color

        pygame.draw.rect(
            self._parent,
            current_color,
            self._rect,
            border_radius=90
        )

        if self._has_border:
            pygame.draw.rect(
                self._parent,
                BLACK,
                self._rect,
                width=BORDER_WIDTH,
                border_radius=90
            )

        if self._image:
            self._parent.blit(self._image, (self.x, self.y))

        if self._text:
            self._parent.blit(self._text, self._text_rect)

        if self._is_ready_check is not None and not self._is_ready_check():
            self.draw_not_ready_overlay()
