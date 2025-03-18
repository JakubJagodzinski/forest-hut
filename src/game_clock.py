import pygame

from config import MAX_FPS


class GameClock:
    _instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            self._game_clock = pygame.time.Clock()

            self._is_game_paused = False
            self._game_time = 0.0

            self._delta_time = 0.0

    @property
    def game_time(self):
        return self._game_time

    @property
    def is_game_paused(self):
        return self._is_game_paused

    def pause(self):
        self._is_game_paused = True

    def resume(self):
        self._is_game_paused = False

    def switch_game_pause(self):
        self._is_game_paused = not self._is_game_paused

    def tick(self) -> float:
        self._delta_time = self._game_clock.tick(MAX_FPS) / 1_000
        return self._delta_time

    def update(self):
        if not self._is_game_paused:
            self._game_time += self._delta_time
