import os

import pygame

from src.common_utils import remove_filename_extension
from src.enums.sprite_state import SpriteState
from src.paths import DIR_ASSETS_SPRITES_OBJECTS
from src.sprites.entity_sprite import EntitySprite
from src.sprites.spritesheet_functions import extract_frames_from_spritesheet


class ObjectSprite(EntitySprite):
    CONTINUOUS_STATES = [
        SpriteState.IDLE,
        SpriteState.FINAL
    ]

    def __init__(self, game_surface, sprite_name, draw_size):
        super().__init__(game_surface, sprite_name, draw_size)

    @classmethod
    def load_sprites(cls, draw_size):
        sprites_names = os.listdir(DIR_ASSETS_SPRITES_OBJECTS)
        for sprite_name in sprites_names:
            if sprite_name not in cls._states:
                cls._states[sprite_name] = {}
                sprites_directory = os.path.join(DIR_ASSETS_SPRITES_OBJECTS, sprite_name)
                states = os.listdir(sprites_directory)
                for state in states:
                    spritesheet = pygame.image.load(os.path.join(sprites_directory, state)).convert_alpha()
                    frames = extract_frames_from_spritesheet(spritesheet, draw_size)
                    cls._states[sprite_name][remove_filename_extension(state)] = frames

    def get_current_state_frames_quantity(self):
        if self.current_disposable_state is not None:
            return len(self._states[self.sprite_name][self.current_disposable_state])
        else:
            return len(self._states[self.sprite_name][self.current_continuous_state])

    def get_current_frame(self):
        if self.current_disposable_state is not None:
            return self._states[self.sprite_name][self.current_disposable_state][self.current_frame_nr]
        else:
            return self._states[self.sprite_name][self.current_continuous_state][self.current_frame_nr]
