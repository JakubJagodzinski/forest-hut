import textwrap

from src.colors import GRAY, WHITE
from src.common_utils import load_txt
from src.fonts import FONT_MONOSPACE_COURIER_16
from src.interface.interface_constants import WINDOW_DEFAULT_STRIPE_HEIGHT
from src.interface.scrollable_window import ScrollableWindow


class TextWindow(ScrollableWindow):
    MARGIN = 10

    def __init__(self, game_surface, x, y, width, height, color=GRAY, stripe_height=WINDOW_DEFAULT_STRIPE_HEIGHT,
                 name='', message='', message_file_path=''):
        super().__init__(
            game_surface,
            x=x,
            y=y,
            width=width,
            height=height,
            max_row_offset_function=self.get_max_row_offset,
            color=color,
            stripe_height=stripe_height,
            name=name
        )
        self.message_font = FONT_MONOSPACE_COURIER_16
        self.message_lines = []
        self.chars_in_line = (self.content_rect.width - (2 * self.MARGIN)) // self.message_font.size('a')[0]
        self.prepare_text_content(message, message_file_path)
        self.lines_in_window = self.content_rect.height // self.message_font.size('a')[1]
        self.line_height = self.content_rect.height // self.lines_in_window

    def get_max_row_offset(self):
        return max(0, len(self.message_lines) - self.lines_in_window)

    def prepare_text_content(self, message, message_file_path):
        if message == '':
            message = load_txt(message_file_path)
        chunks = message.split('\n')
        wrapped_message = []
        for line_nr, line in enumerate(chunks):
            wrapped_line = textwrap.wrap(line, width=self.chars_in_line)
            if len(wrapped_line) > 1:
                for new_line in wrapped_line:
                    wrapped_message.append(new_line)
            else:
                wrapped_message.append(line)
        for line in wrapped_message:
            self.message_lines.append(self.message_font.render(line, True, WHITE))

    def draw_text(self):
        for message_line_nr in range(self._row_offset, len(self.message_lines)):
            message_line = self.message_lines[message_line_nr]
            line_height = message_line.get_height()
            message_line_y = self.content_rect.y + ((message_line_nr - self._row_offset) * line_height)
            if message_line_y + line_height >= self.content_rect.y + self.content_rect.height:
                return
            self.game_surface.blit(message_line, (self.content_rect.x + TextWindow.MARGIN, message_line_y))

    def draw(self):
        super().draw(len(self.message_lines), self.lines_in_window)
        if self.is_open:
            self.draw_text()
