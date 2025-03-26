import pygame

from project_info import _PROJECT_NAME
from src.enums.game_mode import GameMode
from src.game_clock import GameClock
from src.managers.core.accounts_manager import AccountsManager
from src.managers.core.mouse_manager import MouseManager
from src.managers.core.sound_manager import SoundManager
from src.paths import PATH_IMAGE_LOGO
from src.screens.screen_manager import ScreenManager


class GameContext:
    _instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_mode):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            self.game_mode = game_mode

            self._screen_surface = self.init_game_resources()
            self._game_surface = pygame.Surface(
                (
                    self._screen_surface.get_width(),
                    self._screen_surface.get_height(),
                ),
                pygame.SRCALPHA
            )

            self.game_clock = GameClock()

            self.sound_manager = SoundManager()
            self.mouse_manager = MouseManager(self.game_surface)
            self.accounts_manager = AccountsManager()
            self.screen_manager = ScreenManager()

    @property
    def is_in_debug_mode(self):
        return self.game_mode == GameMode.DEBUG

    @property
    def game_surface(self):
        return self._game_surface

    @property
    def screen_surface(self):
        return self._screen_surface

    @staticmethod
    def init_game_resources() -> [pygame.Surface, pygame.Surface]:
        pygame.init()

        pygame.display.set_caption(_PROJECT_NAME)
        pygame.display.set_icon(pygame.image.load(PATH_IMAGE_LOGO))

        screen_info = pygame.display.Info()
        SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

        screen_surface = pygame.display.set_mode(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            ),
            #pygame.FULLSCREEN |
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        return screen_surface
