from src.enums.game_mode import GameMode
from src.enums.screen_type import ScreenType
from src.game_context import GameContext
from src.screens.screen_manager import ScreenManager


def run_game():
    game_context = GameContext(GameMode.STANDARD)

    screen_manager = ScreenManager.get_instance()
    screen_manager.next_screen = ScreenType.LOGIN

    while True:
        screen_manager.enter_next_screen()
