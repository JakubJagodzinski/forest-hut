import os

import pygame

from src.common_utils import remove_filename_extension
from src.enums.entity_marker_type import EntityMarkerType
from src.paths import DIR_ASSETS_NPC_MARKERS

ENTITY_MARKER_PRIORITIES = {
    EntityMarkerType.COMPLETED_QUEST: 1,
    EntityMarkerType.NEW_QUEST: 2,
    EntityMarkerType.BANKER: 3,
    EntityMarkerType.VENDOR: 4,
}


class EntityMarker:
    game_clock = None

    _markers = {}
    MARKER_SIZE = 60
    MARKER_Y_OFFSET = 10

    MARKER_MOVE_RANGE = 10
    MARKER_MOVE_SPEED_IN_SECONDS = 0.03

    def __init__(self, game_surface, entity_draw_size, marker_name):
        self.game_surface = game_surface
        self.entity_draw_size = entity_draw_size
        self.marker = self._markers[marker_name]
        self.is_moving_up = True
        self.current_offset = 0
        self.offset_last_change_time = 0.0

    @classmethod
    def setup_references(cls):
        from src.game_clock import GameClock

        cls.game_clock = GameClock.get_instance()

    @classmethod
    def load_entity_markers(cls):
        marker_names = os.listdir(DIR_ASSETS_NPC_MARKERS)
        for marker_name in marker_names:
            marker_image = pygame.image.load(os.path.join(DIR_ASSETS_NPC_MARKERS, marker_name)).convert_alpha()
            marker_image = pygame.transform.scale(marker_image, (cls.MARKER_SIZE, cls.MARKER_SIZE))
            cls._markers[remove_filename_extension(marker_name)] = marker_image

    @property
    def is_change_marker_offset_ready(self):
        return (self.game_clock.game_time - self.offset_last_change_time) > self.MARKER_MOVE_SPEED_IN_SECONDS

    def change_offset(self):
        if self.is_change_marker_offset_ready:
            self.offset_last_change_time = self.game_clock.game_time
            if not self.game_clock.is_game_paused:
                if self.current_offset == self.MARKER_MOVE_RANGE:
                    self.is_moving_up = False
                if self.current_offset < 0:
                    self.is_moving_up = True
                if self.is_moving_up:
                    self.current_offset += 1
                else:
                    self.current_offset -= 1

    def draw_entity_marker(self, screen_position):
        self.game_surface.blit(
            self.marker,
            (
                screen_position[0] - (self.MARKER_SIZE // 2),
                screen_position[1] - self.entity_draw_size - self.MARKER_Y_OFFSET + self.current_offset
            )
        )
        self.change_offset()
