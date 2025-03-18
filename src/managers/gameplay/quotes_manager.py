import random
import textwrap

import pygame

from src.colors import WHITE, BLACK
from src.common_utils import load_json
from src.enums.quote_type import QuoteType
from src.fonts import FONT_MONOSPACE_COURIER_16
from src.interface.interface_constants import BORDER_WIDTH
from src.paths import PATH_JSON_ENEMY_COMMON_QUOTES, PATH_JSON_NPC_COMMON_QUOTES, PATH_JSON_PLAYER_COMMON_QUOTES, \
    PATH_JSON_RETURN_TO_TOWN_QUOTES


class Quote:
    DRAW_SECONDS_PER_CHAR = 0.07
    MAX_CHARS_IN_LINE = 40

    QUOTE_LINES_OFFSET_Y = 2
    QUOTE_WINDOW_TEXT_PADDING_X = 5

    QUOTE_FONT = FONT_MONOSPACE_COURIER_16

    game_clock = None

    def __init__(self, game_surface, speaker_reference, speaker_draw_size, quote):
        self.game_surface = game_surface
        self.speaker_reference = speaker_reference
        self.speaker_draw_size = speaker_draw_size

        self.quote_lines = self._split_quote_to_lines(quote, WHITE)

        self.quote_draw_start_time = self.game_clock.game_time
        self.quote_draw_time = self.DRAW_SECONDS_PER_CHAR * len(quote)

    @classmethod
    def setup_references(cls):
        from src.game_clock import GameClock

        cls.game_clock = GameClock.get_instance()

    def is_quote_time_over(self):
        return self.speaker_reference.is_dead or (
                (self.game_clock.game_time - self.quote_draw_start_time) > self.quote_draw_time)

    def get_speaker_reference(self):
        return self.speaker_reference

    @classmethod
    def _split_quote_to_lines(cls, quote: str, quote_color: tuple) -> list:
        quote_chunks = textwrap.wrap(quote, width=cls.MAX_CHARS_IN_LINE)
        quote_lines = []
        for quote_chunk in quote_chunks:
            quote_lines.append(cls.QUOTE_FONT.render(quote_chunk, False, quote_color))
        return quote_lines

    def draw(self) -> None:
        quote_window_width = (max(quote_line.get_width() for quote_line in self.quote_lines)
                              + (2 * self.QUOTE_WINDOW_TEXT_PADDING_X))
        quote_window_height = self.QUOTE_FONT.get_height() * len(self.quote_lines)

        quote_window_x = (self.speaker_reference.x
                          - (self.speaker_draw_size // 2)
                          - ((quote_window_width - self.speaker_draw_size) // 2))
        quote_window_y = (self.speaker_reference.y
                          - (self.speaker_draw_size // 2)
                          - quote_window_height)

        quote_window_screen_x, quote_window_screen_y = self.speaker_reference.map_manager.convert_map_position_to_screen_position(
            quote_window_x, quote_window_y
        )

        # draw quote window background
        pygame.draw.rect(
            self.game_surface,
            BLACK,
            (
                quote_window_screen_x,
                quote_window_screen_y,
                quote_window_width,
                quote_window_height
            ),
            border_radius=90
        )

        # draw quote window border
        pygame.draw.rect(
            self.game_surface,
            WHITE,
            (
                quote_window_screen_x,
                quote_window_screen_y,
                quote_window_width,
                quote_window_height
            ),
            width=BORDER_WIDTH,
            border_radius=90
        )

        # draw quote text
        for line_nr, quote_text in enumerate(self.quote_lines):
            quote_x = quote_window_screen_x + self.QUOTE_WINDOW_TEXT_PADDING_X
            quote_y = quote_window_screen_y + (line_nr * (quote_text.get_height() + self.QUOTE_LINES_OFFSET_Y))
            self.game_surface.blit(quote_text, (quote_x, quote_y))


class QuotesManager:
    _instance = None

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

            self.game_surface = game_surface

            enemy_common_quotes = load_json(PATH_JSON_ENEMY_COMMON_QUOTES)
            npc_common_quotes = load_json(PATH_JSON_NPC_COMMON_QUOTES)
            player_common_quotes = load_json(PATH_JSON_PLAYER_COMMON_QUOTES)
            return_to_town_quotes = load_json(PATH_JSON_RETURN_TO_TOWN_QUOTES)

            self.quotes = {
                QuoteType.PLAYER: player_common_quotes,
                QuoteType.ENEMY: enemy_common_quotes,
                QuoteType.NPC: npc_common_quotes,
                QuoteType.RETURN_TO_TOWN: return_to_town_quotes
            }

            self._quotes_queue = []

    def clear_quotes_queue(self):
        self._quotes_queue.clear()

    def _has_speaker_already_queued_quote(self, speaker_reference) -> bool:
        for quote_entry in self._quotes_queue:
            if speaker_reference == quote_entry.get_speaker_reference():
                return True
        return False

    def get_random_common_quote(self, quote_type) -> str:
        return random.choice(self.quotes[quote_type])

    def push_quote_to_queue(self, quote_type, speaker_reference, speaker_draw_size, quote=None) -> None:
        if not self._has_speaker_already_queued_quote(speaker_reference):
            if quote is None:
                quote = self.get_random_common_quote(quote_type)
            quote_entry = Quote(
                game_surface=self.game_surface,
                speaker_reference=speaker_reference,
                speaker_draw_size=speaker_draw_size,
                quote=quote
            )
            self._quotes_queue.append(quote_entry)

    def draw_quotes(self) -> None:
        quotes_to_delete = []
        for quote in self._quotes_queue:
            if quote.is_quote_time_over():
                quotes_to_delete.append(quote)
            else:
                quote.draw()

        for entry in quotes_to_delete:
            self._quotes_queue.remove(entry)
