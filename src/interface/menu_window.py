import os

import pygame

from src.colors import GRAY_GREEN, BLACK, GRAY, WHITE
from src.fonts import FONT_ALICE_IN_WONDERLAND_48, FONT_ARIAL_16
from src.interface.button import Button
from src.interface.interface_constants import MENU_BUTTON_HEIGHT, MENU_BUTTON_WIDTH
from src.interface.text_window import TextWindow
from src.interface.window import Window
from src.managers.core.sound_manager import SoundManager
from src.paths import DIR_WHATSNEW


class MenuWindow(Window):
    game_clock = None

    def __init__(self, game_surface, interface_manager):
        width = (game_surface.get_width() // 4)
        height = (game_surface.get_height() // 2)
        super().__init__(
            game_surface,
            (game_surface.get_width() // 2) - (width // 2),
            (game_surface.get_height() // 2) - (height // 2),
            width,
            height,
            name='MENU'
        )
        self.interface_manager = interface_manager
        self.font = FONT_ARIAL_16
        popup_window_width = (self.game_surface.get_width() // 2)
        popup_window_height = self.rect.height
        popup_window_x = (self.game_surface.get_width() // 2) - (popup_window_width // 2)
        popup_window_y = self.rect.y

        next_button_offset = MENU_BUTTON_HEIGHT + 10
        menu_window_middle_x = (self.game_surface.get_width() // 2)
        menu_window_buttons_start = self.content_rect.y + MENU_BUTTON_HEIGHT

        resume_button = Button(
            game_surface=game_surface,
            center_x=menu_window_middle_x,
            center_y=menu_window_buttons_start,
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            button_color=GRAY_GREEN,
            text_color=BLACK,
            font=self.font,
            action=self.switch_open,
            text='RESUME'
        )
        self._buttons.append(resume_button)

        self.whatsnew_window = TextWindow(
            self.game_surface,
            x=popup_window_x,
            y=popup_window_y,
            width=popup_window_width,
            height=popup_window_height,
            color=GRAY,
            name='WHAT\'S NEW?',
            message_file_path=os.path.join(DIR_WHATSNEW, '0.1.0.txt')
        )
        whatsnew_button = Button(
            game_surface=self.game_surface,
            center_x=menu_window_middle_x,
            center_y=menu_window_buttons_start + next_button_offset,
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            button_color=GRAY_GREEN,
            text_color=BLACK,
            font=self.font,
            action=self.whatsnew_window.switch_open,
            text='WHAT\'S NEW?'
        )
        self._buttons.append(whatsnew_button)

        self.controls_window = Window(
            self.game_surface,
            x=popup_window_x,
            y=popup_window_y,
            width=popup_window_width,
            height=popup_window_height,
            color=GRAY,
            name='CONTROLS'
        )
        controls_button = Button(
            game_surface=self.game_surface,
            center_x=menu_window_middle_x,
            center_y=menu_window_buttons_start + (2 * next_button_offset),
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            button_color=GRAY_GREEN,
            text_color=BLACK,
            font=self.font,
            action=self.controls_window.switch_open,
            text='CONTROLS'
        )
        self._buttons.append(controls_button)

        save_button = Button(
            game_surface=game_surface,
            center_x=menu_window_middle_x,
            center_y=menu_window_buttons_start + (3 * next_button_offset),
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            button_color=GRAY_GREEN,
            text_color=BLACK,
            font=self.font,
            action=self.interface_manager.save_game,
            text='SAVE'
        )
        self._buttons.append(save_button)

        quit_game_button = Button(
            game_surface=game_surface,
            center_x=menu_window_middle_x,
            center_y=menu_window_buttons_start + (4 * next_button_offset),
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            button_color=GRAY_GREEN,
            text_color=BLACK,
            font=self.font,
            action=self.try_quit_game,
            text='QUIT GAME'
        )
        self._buttons.append(quit_game_button)

        quit_to_desktop_button = Button(
            game_surface=game_surface,
            center_x=menu_window_middle_x,
            center_y=menu_window_buttons_start + (5 * next_button_offset),
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            button_color=GRAY_GREEN,
            text_color=BLACK,
            font=self.font,
            action=self.try_quit_to_desktop,
            text='QUIT TO DESKTOP'
        )
        self._buttons.append(quit_to_desktop_button)

        self._game_paused_overlay = pygame.Surface((game_surface.get_width(), game_surface.get_height()))
        self._game_paused_overlay.fill((0, 0, 0))
        self._game_paused_overlay.set_alpha(170)

        self.game_paused_text = FONT_ALICE_IN_WONDERLAND_48.render('GAME PAUSED', False, WHITE)
        self.game_paused_y = (self.rect.y // 2) - (self.game_paused_text.get_height() // 2)
        self.game_paused_x = (game_surface.get_width() // 2) - (self.game_paused_text.get_width() // 2)

    @classmethod
    def setup_references(cls):
        from src.game_clock import GameClock

        cls.game_clock = GameClock.get_instance()

    def try_quit_game(self):
        self.interface_manager.open_choice_window(
            'Are you sure you want to quit game?',
            self.interface_manager.quit_game
        )

    def try_quit_to_desktop(self):
        self.interface_manager.open_choice_window(
            'Are you sure you want to quit to desktop?',
            self.interface_manager.quit_to_desktop
        )

    def handle_mouse_events(self, event) -> bool:
        if self.whatsnew_window.is_open:
            if self.whatsnew_window.handle_mouse_events(event):
                return True
        elif self.controls_window.is_open:
            if self.controls_window.handle_mouse_events():
                return True
        elif super().handle_mouse_events():
            return True
        return False

    def switch_open(self) -> None:
        super().switch_open()
        if not self.is_open:
            self.whatsnew_window.close()
            self.controls_window.close()
        SoundManager.switch_soundtrack_pause()
        self.game_clock.switch_game_pause()

    def _draw_game_paused_overlay(self) -> None:
        self.game_surface.blit(self._game_paused_overlay, (0, 0))

    def draw_game_paused_text(self) -> None:
        self.game_surface.blit(self.game_paused_text, (self.game_paused_x, self.game_paused_y))

    def draw(self) -> None:
        if self.is_open:
            self._draw_game_paused_overlay()

            super().draw()
            self.draw_buttons()

            self.controls_window.draw()
            self.whatsnew_window.draw()

            self.draw_game_paused_text()
