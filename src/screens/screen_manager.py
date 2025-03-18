from src.enums.screen_type import ScreenType
from src.screens.game_screen import GameScreen
from src.screens.login_screen import LoginScreen


class ScreenManager:
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

            self._next_screen = ScreenType.LOGIN

            self.screens = {
                ScreenType.LOGIN: LoginScreen(),
                ScreenType.GAME: GameScreen()
            }

    @property
    def next_screen(self):
        return self._next_screen

    @next_screen.setter
    def next_screen(self, next_screen):
        self._next_screen = next_screen

    def enter_next_screen(self):
        self.screens[self._next_screen].enter()
