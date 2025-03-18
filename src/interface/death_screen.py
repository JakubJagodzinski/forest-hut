import pygame

from src.colors import BLACK, RED
from src.fonts import FONT_ALICE_IN_WONDERLAND_48
from src.interface.button import Button


class DeathScreen:
    HEADER_Y = 200

    BUTTON_OFFSET = 200

    HARDCORE_DEATH_MESSAGE = 'YOUR HERO DIED FOREVER!'
    DEATH_MESSAGE = 'YOU DIED!'

    RESURRECT_HERE_BUTTON_NAME = 'RESURRECT HERE'
    RESURRECT_IN_TOWN_BUTTON_NAME = 'RESURRECT IN TOWN'
    DELETE_CHARACTER_BUTTON_NAME = 'DELETE CHARACTER'

    SCREEN_OVERLAY_ALPHA = 110

    def __init__(self, game_surface, is_game_hardcore, resurrect_here_action, resurrect_in_town_action,
                 delete_character_action):
        self.game_surface = game_surface

        self.screen_overlay = pygame.Surface((self.game_surface.get_width(), self.game_surface.get_height()))
        self.screen_overlay.fill(RED)
        self.screen_overlay.set_alpha(self.SCREEN_OVERLAY_ALPHA)

        self.is_game_hardcore = is_game_hardcore

        if self.is_game_hardcore:
            self.header = FONT_ALICE_IN_WONDERLAND_48.render(self.HARDCORE_DEATH_MESSAGE, False, BLACK)
        else:
            self.header = FONT_ALICE_IN_WONDERLAND_48.render(self.DEATH_MESSAGE, False, BLACK)

        self.header_x = (self.game_surface.get_width() // 2) - (self.header.get_width() // 2)

        self.resurrect_here_button = Button(
            self.game_surface,
            center_x=(self.game_surface.get_width() // 2) + self.BUTTON_OFFSET,
            center_y=(self.game_surface.get_height() // 2) + self.BUTTON_OFFSET,
            action=resurrect_here_action,
            text=self.RESURRECT_HERE_BUTTON_NAME
        )

        self.resurrect_in_town_button = Button(
            self.game_surface,
            center_x=(self.game_surface.get_width() // 2) - self.BUTTON_OFFSET,
            center_y=(self.game_surface.get_height() // 2) + self.BUTTON_OFFSET,
            action=resurrect_in_town_action,
            text=self.RESURRECT_IN_TOWN_BUTTON_NAME
        )

        self.delete_character_button = Button(
            self.game_surface,
            center_x=(self.game_surface.get_width() // 2),
            center_y=(self.game_surface.get_height() // 2) + self.BUTTON_OFFSET,
            action=delete_character_action,
            text=self.DELETE_CHARACTER_BUTTON_NAME
        )

    def handle_mouse_events(self):
        if self.is_game_hardcore:
            return self.delete_character_button.handle_event()
        else:
            return self.resurrect_here_button.handle_event() or self.resurrect_in_town_button.handle_event()

    def draw(self):
        self.game_surface.blit(self.screen_overlay, (0, 0))
        self.game_surface.blit(self.header, (self.header_x, self.HEADER_Y))
        if self.is_game_hardcore:
            self.delete_character_button.draw()
        else:
            self.resurrect_here_button.draw()
            self.resurrect_in_town_button.draw()
