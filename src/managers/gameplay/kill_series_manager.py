from src.colors import RED, WHITE
from src.enums.sound_type import SoundType
from src.fonts import FONT_ALICE_IN_WONDERLAND_40
from src.interface.bar import Bar
from src.interface.interface_constants import XP_BAR_HEIGHT, LOWER_UI_BAR_HEIGHT


class KillSeriesManager:
    _instance = None

    KILL_SERIES_TIME_IN_SECONDS = 6.0

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

            self.game_clock = None
            self.sound_manager = None

            self.kills = 0
            self.last_hit_time = float('-inf')
            self.remaining_time = 0

            Y_OFFSET = 50
            KILL_SERIES_REMAINING_TIME_BAR_WIDTH = (self.game_surface.get_width() // 4)
            KILL_SERIES_REMAINING_TIME_BAR_HEIGHT = 10
            KILL_SERIES_REMAINING_TIME_BAR_X = ((self.game_surface.get_width() // 2)
                                                - (KILL_SERIES_REMAINING_TIME_BAR_WIDTH // 2))
            KILL_SERIES_REMAINING_TIME_BAR_Y = (self.game_surface.get_height()
                                                - LOWER_UI_BAR_HEIGHT
                                                - XP_BAR_HEIGHT
                                                - Y_OFFSET)
            self.remaining_time_bar = Bar(
                game_surface=self.game_surface,
                x=KILL_SERIES_REMAINING_TIME_BAR_X,
                y=KILL_SERIES_REMAINING_TIME_BAR_Y,
                width=KILL_SERIES_REMAINING_TIME_BAR_WIDTH,
                height=KILL_SERIES_REMAINING_TIME_BAR_HEIGHT,
                color=RED,
                parts=4,
                border_radius=90
            )

            self.kills_and_title_font = FONT_ALICE_IN_WONDERLAND_40
            self.kill_series_text = None
            self.kill_series_suffix = ''
            self.kill_series_text_y = KILL_SERIES_REMAINING_TIME_BAR_Y - 50
            self.kill_series_text_x = 0

            from src.database_service import DatabaseService
            self.kill_series_titles = DatabaseService.get_kill_series_titles()
            self.old_title = ''
            self.title_text = None
            self.title_text_x = 0
            self.title_text_y = self.kill_series_text_y - self.kills_and_title_font.get_height() - 10

    def setup_references(self):
        from src.managers.core.sound_manager import SoundManager
        from src.game_clock import GameClock

        self.game_clock = GameClock.get_instance()
        self.sound_manager = SoundManager.get_instance()

    def get_kill_series_title(self) -> str | None:
        for entry in reversed(self.kill_series_titles):
            for title, min_kills in entry.items():
                if self.kills >= min_kills:
                    return title
        return None

    @property
    def kill_series(self):
        return self.kills

    def refresh_kill_series(self) -> None:
        self.last_hit_time = self.game_clock.game_time

    def increment_kill_series(self, enemies_killed: int) -> None:
        self.kills += enemies_killed
        self.update_kill_series_text()
        self.update_title_text()

    def update_kill_series_text(self):
        self.kill_series_suffix = 'kills' if self.kills > 1 else 'kill'
        self.kill_series_text = self.kills_and_title_font.render(
            f'{self.kills} {self.kill_series_suffix}',
            False,
            WHITE
        )
        self.kill_series_text_x = (self.game_surface.get_width() // 2) - (self.kill_series_text.get_width() // 2)

    def update_title_text(self):
        new_kill_series_title = self.get_kill_series_title()
        if new_kill_series_title is not None:
            if new_kill_series_title != self.old_title:
                self.title_text = self.kills_and_title_font.render(
                    new_kill_series_title,
                    False,
                    WHITE
                )
                self.title_text_x = (self.game_surface.get_width() // 2) - (self.title_text.get_width() // 2)
                self.old_title = new_kill_series_title
        else:
            self.title_text = None
            self.old_title = ''

    def handle_kill_series_end(self) -> int:
        self.remaining_time = (self.KILL_SERIES_TIME_IN_SECONDS - (self.game_clock.game_time - self.last_hit_time))
        if self.remaining_time <= 0:
            if self.title_text is not None:
                self.sound_manager.play_sound(SoundType.KILL_SERIES_END)
                bonus_xp = self.kills
            else:
                bonus_xp = 0
            self.kills = 0
            return bonus_xp
        else:
            return 0
