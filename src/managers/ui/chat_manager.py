import textwrap

import pygame

from src.enums.chat_message_color_type import ChatMessageColorType
from src.fonts import FONT_MONOSPACE_COURIER_16
from src.inappropriate_content_filter import InappropriateContentFilter
from src.interface.input_box import InputBox
from src.interface.interface_constants import LOWER_UI_BAR_HEIGHT, XP_BAR_HEIGHT
from src.interface.scrollable_window import ScrollableWindow


class ChatManager(ScrollableWindow):
    _instance = None

    WINDOW_OFFSET = 10
    WIDTH = 400
    HEIGHT = 200

    MARGIN = 5

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_surface):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            super().__init__(
                game_surface,
                x=self.WINDOW_OFFSET,
                y=game_surface.get_height() - LOWER_UI_BAR_HEIGHT - XP_BAR_HEIGHT - self.WINDOW_OFFSET - self.HEIGHT,
                width=self.WIDTH,
                height=self.HEIGHT,
                max_row_offset_function=self.get_max_row_offset,
                action_on_change_row_offset=self.render_chat_messages,
                name='CHAT'
            )

            self.inappropriate_content_filter = InappropriateContentFilter()
            self.game_clock = None
            self.command_manager = None
            self.datetime_manager = None
            self.map_manager = None
            self.player_manager = None

            self.message_font = FONT_MONOSPACE_COURIER_16
            self.messages = []
            self.last_messages = []
            self.last_message_index = 0

            self.lines_in_window = self.content_rect.height // self.message_font.get_height()
            self.line_height = self.content_rect.height // self.lines_in_window
            self.chars_in_line = ((self.content_rect.width
                                   - (2 * self.MARGIN)
                                   - self.SCROLLING_BAR_WIDTH)
                                  // self.message_font.size('a')[0])

            self.rendered_messages = []
            self.render_chat_messages()

            self.input_box = InputBox(
                self.game_surface,
                x=self.rect.x,
                y=self.content_rect.y + self.content_rect.height,
                width=self.rect.width,
                height=self.stripe_height,
                border_radius=90
            )

    def setup_references(self):
        from src.managers.ui.command_manager import CommandManager
        from src.game_clock import GameClock
        from src.managers.gameplay.datetime_manager import DatetimeManager
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.gameplay.player_manager import PlayerManager

        self.player_manager = PlayerManager.get_instance()
        self.map_manager = MapManager.get_instance()
        self.datetime_manager = DatetimeManager.get_instance()
        self.game_clock = GameClock.get_instance()
        self.command_manager = CommandManager.get_instance()

    def get_max_row_offset(self):
        return max(0, len(self.messages) - self.lines_in_window)

    def decrement_last_message_index(self):
        self.last_message_index -= 1
        if self.last_message_index < 0:
            self.last_message_index = len(self.last_messages) - 1

    def increment_last_message_index(self):
        self.last_message_index += 1
        if self.last_message_index >= len(self.last_messages):
            self.last_message_index = 0

    def switch_open_input_box(self):
        self.input_box.switch_active()
        if not self.is_input_box_active():
            self.input_box.clear()

    def switch_open(self):
        super().switch_open()
        if not self.is_open and self.is_input_box_active():
            self.switch_open_input_box()

    def is_input_box_active(self):
        return self.input_box.is_active()

    def maximize_row_offset(self):
        self._row_offset = self.get_max_row_offset()
        self.render_chat_messages()

    def push_message_from_input_box(self):
        message = self.input_box.get_text()
        if len(message) > 0:
            censored_message = self.inappropriate_content_filter.censor_words_in_message(self.input_box.get_text())
            self.push_message_to_chat(censored_message, ChatMessageColorType.PLAYER)
            self.last_messages.append(self.input_box.get_text())
        self.maximize_row_offset()
        self.switch_open_input_box()

    def push_message_to_chat(self, message, message_color=ChatMessageColorType.NORMAL):
        chunks = textwrap.wrap(message, width=self.chars_in_line)
        for chunk in chunks:
            self.messages.append([message_color, chunk])
        self.maximize_row_offset()

    @staticmethod
    def is_command(command: str) -> bool:
        return command.startswith('/')

    def use_command(self, command) -> bool:
        self.last_messages.append(command)
        result = self.command_manager.use_command(command[1:])
        if not result:
            filtered_command = self.inappropriate_content_filter.censor_words_in_message(command[1:])
            self.push_message_to_chat(
                f'Command "{filtered_command}" not found.',
                ChatMessageColorType.ERROR
            )
        return result

    def handle_keyboard_events(self, event):
        if self.input_box.is_active():
            if event.key == pygame.K_ESCAPE:
                if self.is_input_box_active():
                    self.switch_open_input_box()
                    return True
            if event.key == pygame.K_RETURN:
                if self.is_command(self.input_box.get_text()):
                    self.use_command(self.input_box.get_text())
                    self.switch_open_input_box()
                else:
                    self.push_message_from_input_box()
                return True
            if event.key == pygame.K_UP:
                if len(self.last_messages) > 0:
                    self.increment_last_message_index()
                    self.input_box.set_text(self.last_messages[self.last_message_index])
                    return True
            elif event.key == pygame.K_DOWN:
                if len(self.last_messages) > 0:
                    self.decrement_last_message_index()
                    self.input_box.set_text(self.last_messages[self.last_message_index])
                    return True
            if self.input_box.handle_events(event):
                return True
        return False

    def get_current_visible_messages_range(self) -> (int, int):
        first_message_index = self._row_offset
        last_message_index = min(len(self.messages), self._row_offset + self.lines_in_window)
        return first_message_index, last_message_index

    def render_chat_messages(self):
        self.rendered_messages = []
        first_message_index, last_message_index = self.get_current_visible_messages_range()
        for message_index in range(first_message_index, last_message_index):
            message_color = self.messages[message_index][0]
            message_content = self.messages[message_index][1]
            rendered_message = self.message_font.render(message_content, False, message_color.value)
            self.rendered_messages.append(rendered_message)

    def draw_chat_messages(self):
        for message_nr, message in enumerate(self.rendered_messages):
            self.game_surface.blit(
                message,
                (
                    self.content_rect.x + self.MARGIN,
                    self.content_rect.y + (message_nr * self.line_height)
                )
            )

    def draw_chat(self):
        if super().is_open:
            super().draw(len(self.messages), self.lines_in_window)
            self.draw_chat_messages()
            if self.is_input_box_active():
                self.input_box.draw()
