from abc import abstractmethod


class Screen:

    def __init__(self):
        from src.game_clock import GameClock
        from src.game_context import GameContext
        from src.managers.core.accounts_manager import AccountsManager
        from src.managers.core.mouse_manager import MouseManager
        from src.managers.core.sound_manager import SoundManager
        from src.screens.screen_manager import ScreenManager

        self.game_context = GameContext.get_instance()

        self.game_surface = self.game_context.game_surface
        self.screen_surface = self.game_context.screen_surface

        self.game_clock = GameClock.get_instance()

        self.screen_manager = ScreenManager.get_instance()
        self.mouse_manager = MouseManager.get_instance()
        self.sound_manager = SoundManager.get_instance()
        self.accounts_manager = AccountsManager.get_instance()

    @abstractmethod
    def enter(self):
        pass
