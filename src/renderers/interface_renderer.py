class InterfaceRenderer:

    def __init__(self, game_surface):
        self.game_surface = game_surface

        self.interface_manager = None

        from src.renderers.kill_series_renderer import KillSeriesRenderer
        self.kill_series_renderer = KillSeriesRenderer(game_surface)

    def setup_references(self):
        from src.managers.ui.interface_manager import InterfaceManager
        self.interface_manager = InterfaceManager.get_instance()

    def draw_level(self) -> None:
        self.game_surface.blit(
            self.interface_manager.level_text,
            (
                self.interface_manager.level_text_draw_x,
                self.interface_manager.level_text_draw_y
            )
        )

    def draw(self):
        self.kill_series_renderer.draw()
        self.draw_level()
