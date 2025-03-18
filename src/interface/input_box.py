import pygame

from src.colors import WHITE, BLACK
from src.fonts import FONT_MONOSPACE_COURIER_16
from src.interface.interface_constants import BORDER_WIDTH


class InputBox:
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 20
    TEXT_X_PADDING = 5

    def __init__(self, game_surface, x, y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, color=WHITE, is_password=False,
                 border_radius=0):
        self.game_surface = game_surface
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )
        self.color = color
        self.is_password = is_password
        self.border_radius = border_radius
        self.text = ''
        self.font = FONT_MONOSPACE_COURIER_16
        self.text_max_display_length = (self.rect.width - (2 * InputBox.TEXT_X_PADDING)) // self.font.size('a')[0]
        self.rendered_text = None
        self.render()
        self.active = False

    def get_text(self):
        return self.text.strip()

    def clear(self):
        self.set_text('')

    def render(self):
        visible_text = self.text[-self.text_max_display_length:]
        visible_text = visible_text if not self.is_password else '*' * len(visible_text)
        self.rendered_text = self.font.render(visible_text, False, self.color)

    def is_active(self):
        return self.active

    def switch_active(self):
        self.active = not self.active

    def set_text(self, text):
        self.text = text
        self.render()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.handle_keyboard_events(event):
                return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_events(event)
            return True
        return False

    def handle_mouse_events(self, event):
        self.active = self.rect.collidepoint(event.pos)

    def handle_keyboard_events(self, event) -> bool:
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode
            self.render()
            return True
        self.render()
        return False

    def draw(self):
        # draw black background
        pygame.draw.rect(
            self.game_surface,
            BLACK,
            self.rect,
            border_radius=self.border_radius
        )

        # draw white border
        pygame.draw.rect(
            self.game_surface,
            WHITE,
            self.rect,
            width=BORDER_WIDTH,
            border_radius=self.border_radius
        )

        self.game_surface.blit(
            self.rendered_text,
            (
                self.rect.x + self.TEXT_X_PADDING,
                self.rect.y + (self.rect.height // 2) - (self.rendered_text.get_height() // 2)
            )
        )
