from abc import abstractmethod

import pygame

from src.colors import RED, WHITE
from src.enums.sprite_state import SpriteState
from src.fonts import FONT_MONOSPACE_COURIER_16
from src.interface.interface_constants import BORDER_WIDTH


class EntitySprite:
    _states = {}

    CONTINUOUS_STATES = []

    ANIMATION_SPEED_IN_SECONDS = 0.07

    game_clock = None
    game_context = None

    def __init__(self, game_surface, sprite_name, draw_size):
        self.game_surface = game_surface
        self.sprite_name = sprite_name
        self.sprite_name_text = FONT_MONOSPACE_COURIER_16.render(self.sprite_name, True, WHITE)
        self.draw_size = draw_size
        self.current_continuous_state = SpriteState.IDLE
        self.current_disposable_state = None
        self.current_frame_nr = 0
        self.last_current_frame_nr_increment_time = 0.0

    @classmethod
    def setup_references(cls):
        from src.game_clock import GameClock
        from src.game_context import GameContext

        cls.game_context = GameContext.get_instance()
        cls.game_clock = GameClock.get_instance()

    @classmethod
    @abstractmethod
    def load_sprites(cls, draw_size):
        pass

    @abstractmethod
    def get_current_frame(self):
        pass

    @abstractmethod
    def get_current_state_frames_quantity(self):
        pass

    def set_sprite_state(self, state):
        if state in self.CONTINUOUS_STATES:
            if state != self.current_continuous_state:
                self.current_continuous_state = state
                self.current_frame_nr = 0
                self.last_current_frame_nr_increment_time = self.game_clock.game_time
        else:
            if state != self.current_disposable_state:
                self.current_disposable_state = state
                self.current_frame_nr = 0
                self.last_current_frame_nr_increment_time = self.game_clock.game_time

    @property
    def is_increment_frame_nr_ready(self):
        return (self.game_clock.game_time
                - self.last_current_frame_nr_increment_time) > self.ANIMATION_SPEED_IN_SECONDS

    def increment_current_frame_nr(self):
        if self.is_increment_frame_nr_ready:
            self.current_frame_nr += 1
            if self.current_frame_nr >= self.get_current_state_frames_quantity():
                if self.current_disposable_state is not None:
                    self.current_disposable_state = None
                self.current_frame_nr = 0
            self.last_current_frame_nr_increment_time = self.game_clock.game_time

    def draw_area_rectangle(self, screen_position):
        draw_x, draw_y = screen_position
        draw_position = (draw_x - (self.draw_size // 2),
                         draw_y - (self.draw_size // 2))
        pygame.draw.rect(
            self.game_surface,
            RED,
            (
                draw_position[0],
                draw_position[1],
                self.draw_size,
                self.draw_size
            ),
            width=BORDER_WIDTH
        )

        pygame.draw.rect(
            self.game_surface,
            WHITE,
            (
                draw_x - 5,
                draw_y - 5,
                10,
                10
            ),
        )
        self.game_surface.blit(self.sprite_name_text, draw_position)

    def draw(self, screen_position):
        screen_x, screen_y = screen_position

        self.game_surface.blit(
            self.get_current_frame(),
            (
                screen_x - (self.draw_size // 2),
                screen_y - (self.draw_size // 2)
            )
        )

        self.increment_current_frame_nr()

        if self.game_context.is_in_debug_mode:
            self.draw_area_rectangle(screen_position)
