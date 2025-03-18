import textwrap

from src.colors import GREEN, BLACK, RED, WHITE
from src.fonts import FONT_ARIAL_18
from src.interface.button import Button
from src.interface.window import Window


class ChoiceWindow(Window):
    _instance = None

    WIDTH = 500
    MIN_HEIGHT = 200

    MAX_CHARS_IN_LINE = 50

    MESSAGE_Y_POSITION_OFFSET = 10

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

            self.message_font = FONT_ARIAL_18
            self.message_lines = []

            height = self.MIN_HEIGHT + (len(self.message_lines) * self.message_font.get_height())
            super().__init__(
                game_surface=game_surface,
                x=(game_surface.get_width() // 2) - (ChoiceWindow.WIDTH // 2),
                y=(game_surface.get_height() // 2) - (height // 2),
                width=ChoiceWindow.WIDTH,
                height=height,
                name='CONFIRM',
                closable=False
            )

            self.window_middle_x = self.content_rect.x + (ChoiceWindow.WIDTH // 2)
            self.message_start_y = self.content_rect.y + self.MESSAGE_Y_POSITION_OFFSET

            self.callback = None

            button_height = 30
            button_width = 2 * button_height
            buttons_y = (self.content_rect.y
                         + self.content_rect.height
                         - (2 * button_height))

            self._buttons = [
                Button(
                    game_surface=self.game_surface,
                    center_x=self.content_rect.x + button_width,
                    center_y=buttons_y,
                    action=self.perform_action,
                    width=button_width,
                    height=button_height,
                    text='YES',
                    button_color=GREEN,
                    text_color=BLACK,
                    with_border=True
                ),
                Button(
                    game_surface=self.game_surface,
                    center_x=self.content_rect.x + self.content_rect.width - (2 * button_width),
                    center_y=buttons_y,
                    action=self.close,
                    width=button_width,
                    height=button_height,
                    text='NO',
                    button_color=RED,
                    text_color=BLACK,
                    with_border=True
                )
            ]

    def set_message(self, message):
        self.message_lines = []
        chunks = textwrap.wrap(message, width=self.MAX_CHARS_IN_LINE)
        for chunk in chunks:
            self.message_lines.append(self.message_font.render(chunk, True, WHITE))

    def open(self, message, callback):
        self.set_message(message)
        self.callback = callback
        super().open()

    def perform_action(self):
        self.callback()

    def draw_message(self):
        for message_line_nr, message_line in enumerate(self.message_lines):
            self.game_surface.blit(
                message_line,
                (
                    self.window_middle_x - (message_line.get_width() // 2),
                    self.message_start_y + (message_line_nr * message_line.get_height())
                )
            )

    def draw(self):
        if self.is_open:
            super().draw()
            self.draw_message()
