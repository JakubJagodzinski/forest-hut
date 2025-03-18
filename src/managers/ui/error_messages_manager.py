from src.colors import LIGHT_RED
from src.fonts import FONT_ARIAL_26


class ErrorMessagesManager:
    _instance = None

    POSITION_Y = 120
    MESSAGES_OFFSET_Y = 5

    MESSAGE_DISPLAY_TIME_IN_SECONDS = 5.0

    MESSAGES_BUFFER_SIZE = 3

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

            self.game_clock = None

            self.game_surface = game_surface
            self.message_font = FONT_ARIAL_26
            self.messages = []

    def setup_references(self):
        from src.game_clock import GameClock

        self.game_clock = GameClock.get_instance()

    def push_message_to_queue(self, message) -> None:
        if len(self.messages) == self.MESSAGES_BUFFER_SIZE:
            self.messages.pop(self.MESSAGES_BUFFER_SIZE - 1)
        self.messages.insert(0, [message, self.game_clock.game_time])

    def draw_error_messages(self):
        messages_to_remove = []
        for message_nr, message in enumerate(self.messages):
            time_left = self.MESSAGE_DISPLAY_TIME_IN_SECONDS - (self.game_clock.game_time - message[1])
            if time_left <= 0:
                messages_to_remove.append(message_nr)
            else:
                alpha = max(0, min(255, int((time_left / self.MESSAGE_DISPLAY_TIME_IN_SECONDS) * 255)))
                message_text = self.message_font.render(message[0], True, LIGHT_RED)
                message_text.set_alpha(alpha)
                self.game_surface.blit(
                    message_text,
                    (
                        (self.game_surface.get_width() // 2) - (message_text.get_width() // 2),
                        self.POSITION_Y + (message_nr * (message_text.get_height() + self.MESSAGES_OFFSET_Y))
                    )
                )
        for message_index in messages_to_remove:
            self.messages.pop(message_index)
