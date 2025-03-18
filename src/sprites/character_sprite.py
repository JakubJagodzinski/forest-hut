import os
from typing import override

import pygame

from src.common_utils import remove_filename_extension
from src.enums.move_direction_type import MoveDirection
from src.enums.sprite_state import SpriteState
from src.paths import DIR_ASSETS_SPRITES_CHARACTERS
from src.sprites.entity_sprite import EntitySprite
from src.sprites.spritesheet_functions import extract_frames_from_spritesheet


class CharacterSprite(EntitySprite):
    CONTINUOUS_STATES = [
        SpriteState.IDLE,
        SpriteState.RUN,
        SpriteState.DEAD,
    ]

    def __init__(self, game_surface, sprite_name, draw_size):
        super().__init__(game_surface, sprite_name, draw_size)
        self._current_direction = MoveDirection.DOWN

    @classmethod
    def load_sprites(cls, draw_size):
        sprites_names = os.listdir(DIR_ASSETS_SPRITES_CHARACTERS)
        for sprite_name in sprites_names:
            if sprite_name not in cls._states:
                cls._states[sprite_name] = {}
                sprites_directory = os.path.join(DIR_ASSETS_SPRITES_CHARACTERS, sprite_name)
                for move_direction in MoveDirection:
                    cls._states[sprite_name][move_direction] = {}
                    direction_directory = os.path.join(sprites_directory, move_direction)
                    states = os.listdir(direction_directory)
                    for state in states:
                        spritesheet = pygame.image.load(os.path.join(direction_directory, state)).convert_alpha()
                        frames = extract_frames_from_spritesheet(spritesheet, draw_size)
                        cls._states[sprite_name][move_direction][remove_filename_extension(state)] = frames

    def set_direction(self, direction):
        self._current_direction = direction

    @override
    def get_current_state_frames_quantity(self):
        if self.current_disposable_state is not None:
            return len(self._states[self.sprite_name][self._current_direction][self.current_disposable_state])
        else:
            return len(self._states[self.sprite_name][self._current_direction][self.current_continuous_state])

    @override
    def get_current_frame(self):
        if self.current_disposable_state is not None:
            return self._states[self.sprite_name][self._current_direction][self.current_disposable_state][
                self.current_frame_nr]
        else:
            return self._states[self.sprite_name][self._current_direction][self.current_continuous_state][
                self.current_frame_nr]
