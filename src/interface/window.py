import pygame

from src.colors import GRAY, RED, BLACK, WHITE
from src.fonts import FONT_ALICE_IN_WONDERLAND_16
from src.interface.button import Button
from src.interface.interface_constants import BORDER_WIDTH, WINDOW_DEFAULT_STRIPE_HEIGHT, WINDOW_DEFAULT_BORDER_RADIUS


class Window:

    def __init__(self, game_surface, x, y, width, height, color=GRAY,
                 stripe_height=WINDOW_DEFAULT_STRIPE_HEIGHT, border_radius=WINDOW_DEFAULT_BORDER_RADIUS,
                 name='', closable=True):
        self.game_surface = game_surface
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.stripe_height = stripe_height
        self.border_radius = border_radius
        self.content_rect = pygame.Rect(
            self.rect.x + BORDER_WIDTH,
            self.rect.y + BORDER_WIDTH + self.stripe_height,
            self.rect.width - (2 * BORDER_WIDTH),
            self.rect.height - (2 * BORDER_WIDTH) - (2 * self.stripe_height)
        )

        self.name_font = FONT_ALICE_IN_WONDERLAND_16
        self.name = None
        self.name_text = None
        self.name_position = None
        self.set_name(name)

        self._buttons = []
        if closable:
            self._buttons.append(
                Button(
                    game_surface=self.game_surface,
                    center_x=(self.rect.x
                              + self.rect.width
                              - (self.stripe_height // 2)),
                    center_y=self.rect.y + (self.stripe_height // 2),
                    action=self.switch_open,
                    width=self.stripe_height,
                    height=self.stripe_height,
                    text='x',
                    button_color=RED,
                    text_color=BLACK,
                    with_border=True
                )
            )

        self._is_open = False

    @property
    def is_hovered(self):
        return self.is_open and self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def is_open(self) -> bool:
        return self._is_open

    def switch_open(self):
        self._is_open = not self._is_open

    def open(self, *args, **kwargs):
        self._is_open = True

    def close(self):
        self._is_open = False

    def set_name(self, name):
        self.name = name
        self.name_text = self.name_font.render(name, False, WHITE)
        name_offset_x = (self.rect.width // 2) - (self.name_text.get_width() // 2)
        name_offset_y = (self.stripe_height // 2) - (self.name_text.get_height() // 2)
        self.name_position = (
            self.rect.x + name_offset_x,
            self.rect.y + name_offset_y
        )

    def handle_mouse_events(self, event=None) -> bool:
        if self.is_open:
            for window_button in self._buttons:
                if window_button.handle_event():
                    return True
        return False

    def draw_window(self):
        pygame.draw.rect(
            self.game_surface,
            BLACK,
            self.rect,
            border_radius=self.border_radius
        )

        pygame.draw.rect(
            self.game_surface,
            self.color,
            self.content_rect
        )

    def draw_name(self):
        self.game_surface.blit(self.name_text, self.name_position)

    def draw_buttons(self):
        for window_button in self._buttons:
            window_button.draw()

    def draw(self):
        if self.is_open:
            self.draw_window()
            self.draw_name()
            self.draw_buttons()
