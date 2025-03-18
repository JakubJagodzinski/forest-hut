import pygame

from src.colors import GRAY, BLACK
from src.interface.interface_constants import WINDOW_DEFAULT_STRIPE_HEIGHT, WINDOW_DEFAULT_BORDER_RADIUS
from src.interface.window import Window
from src.managers.core.mouse_manager import MouseManager


class ScrollableWindow(Window):
    SCROLLING_BAR_WIDTH = 5

    def __init__(
            self,
            game_surface,
            x,
            y,
            width,
            height,
            max_row_offset_function,
            action_on_change_row_offset=None,
            color=GRAY,
            stripe_height=WINDOW_DEFAULT_STRIPE_HEIGHT,
            border_radius=WINDOW_DEFAULT_BORDER_RADIUS,
            name=''
    ):
        super().__init__(game_surface, x, y, width, height, color, stripe_height, border_radius, name)
        self.max_row_offset_function = max_row_offset_function
        self.action_on_change_row_offset = action_on_change_row_offset
        self._row_offset = 0
        self.scrolling_bar_width_offset = self.SCROLLING_BAR_WIDTH + (self.SCROLLING_BAR_WIDTH // 2)

    def _increase_row_offset(self) -> None:
        self._row_offset = min(self.max_row_offset_function(), self._row_offset + 1)
        if self.action_on_change_row_offset is not None:
            self.action_on_change_row_offset()

    def _decrease_row_offset(self) -> None:
        self._row_offset = max(0, self._row_offset - 1)
        if self.action_on_change_row_offset is not None:
            self.action_on_change_row_offset()

    def is_scrollable_area_hovered(self):
        return self.content_rect.collidepoint(pygame.mouse.get_pos())

    def handle_scrolling_event(self, event):
        if self.is_scrollable_area_hovered():
            if MouseManager.is_scrolled_up(event):
                self._decrease_row_offset()
            elif MouseManager.is_scrolled_down(event):
                self._increase_row_offset()

    def handle_mouse_events(self, event) -> bool:
        if super().handle_mouse_events(event):
            return True
        if self.handle_scrolling_event(event):
            return True
        return False

    def draw_scrolling_bar(self, max_content, content_in_window):
        if max_content > content_in_window:
            scroll_ratio = max(0.0, min(1.0, self._row_offset / self.max_row_offset_function()))
            content_height = self.content_rect.height + max(0, max_content - content_in_window) * (
                    self.content_rect.height / content_in_window)
            scrolling_bar_height = max(10, (self.content_rect.height / content_height) * self.content_rect.height)
            scrolling_bar_y = self.content_rect.y + scroll_ratio * (self.content_rect.height - scrolling_bar_height)
            pygame.draw.rect(
                self.game_surface,
                BLACK,
                (
                    self.content_rect.x + self.content_rect.width - self.scrolling_bar_width_offset,
                    scrolling_bar_y,
                    self.SCROLLING_BAR_WIDTH,
                    scrolling_bar_height
                ),
                border_radius=45
            )

    def draw(self, max_content, content_in_window):
        if self.is_open:
            super().draw()
            self.draw_scrolling_bar(max_content, content_in_window)
