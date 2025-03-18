class KillSeriesRenderer:

    def __init__(self, game_surface):
        self.game_surface = game_surface
        self.kill_series_manager = None

    def setup_references(self):
        from src.managers.gameplay.kill_series_manager import KillSeriesManager
        self.kill_series_manager = KillSeriesManager.get_instance()

    def draw(self) -> None:
        if self.kill_series_manager.kill_series > 0:

            self.game_surface.blit(
                self.kill_series_manager.kill_series_text,
                (
                    self.kill_series_manager.kill_series_text_x,
                    self.kill_series_manager.kill_series_text_y
                )
            )

            title_text = self.kill_series_manager.title_text
            if title_text is not None:
                self.game_surface.blit(
                    title_text,
                    (
                        self.kill_series_manager.title_text_x,
                        self.kill_series_manager.title_text_y
                    )
                )

            self.kill_series_manager.remaining_time_bar.draw(
                int(self.kill_series_manager.remaining_time * 100),
                int(self.kill_series_manager.KILL_SERIES_TIME_IN_SECONDS * 100)
            )
