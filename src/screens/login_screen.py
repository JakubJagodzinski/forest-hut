from typing import override

import pygame

from src.colors import WHITE, BLACK
from src.common_utils import quit_game
from src.enums.cursor_type import CursorType
from src.enums.screen_type import ScreenType
from src.fonts import FONT_ALICE_IN_WONDERLAND_18, FONT_ARIAL_18
from src.interface.button import Button
from src.interface.input_box import InputBox
from src.interface.interface_constants import MENU_BUTTON_HEIGHT, MENU_BUTTON_WIDTH
from src.paths import PATH_IMAGE_START_SCREEN, PATH_IMAGE_NAME
from project_info import _PROJECT_NAME, _VERSION
from src.screens.screen import Screen


class LoginScreen(Screen):

    def __init__(self):
        super().__init__()

    @override
    def enter(self):
        start_screen_image = pygame.image.load(PATH_IMAGE_START_SCREEN).convert()
        start_screen_image = pygame.transform.scale(
            start_screen_image,
            (
                self.game_surface.get_height(),
                self.game_surface.get_height()
            )
        )
        start_screen_image_x = (self.game_surface.get_width() // 2) - (start_screen_image.get_width() // 2)
        start_screen_image_position = (start_screen_image_x, 0)

        name_image = pygame.image.load(PATH_IMAGE_NAME).convert_alpha()
        name_image = pygame.transform.scale(name_image, (200, 50))
        name_image_x = (self.game_surface.get_width() // 2) - (name_image.get_width() // 2)
        name_image_y = 50
        name_image_position = (name_image_x, name_image_y)

        account_name_text_box = InputBox(
            self.game_surface,
            x=(self.game_surface.get_width() // 2) - (InputBox.DEFAULT_WIDTH // 2),
            y=(5 * self.game_surface.get_height() // 8) - InputBox.DEFAULT_HEIGHT
        )

        password_text_box = InputBox(
            self.game_surface,
            x=(self.game_surface.get_width() // 2) - (InputBox.DEFAULT_WIDTH // 2),
            y=(5 * self.game_surface.get_height() // 8) + InputBox.DEFAULT_HEIGHT,
            is_password=True
        )

        input_boxes = [
            account_name_text_box,
            password_text_box
        ]

        def login():
            account_name = account_name_text_box.get_text()
            password = password_text_box.get_text()
            return self.accounts_manager.authorize(account_name, password)

        buttons_left_section_x = self.game_surface.get_width() - (
                (self.game_surface.get_width() - start_screen_image.get_height()) // 4)

        quit_button = Button(
            self.game_surface,
            buttons_left_section_x,
            MENU_BUTTON_HEIGHT,
            width=MENU_BUTTON_WIDTH,
            height=MENU_BUTTON_HEIGHT,
            action=quit_game,
            text='QUIT',
            font=FONT_ALICE_IN_WONDERLAND_18
        )

        login_button = Button(
            self.game_surface,
            center_x=(self.game_surface.get_width() // 2),
            center_y=(5 * self.game_surface.get_height() // 8) + (3 * InputBox.DEFAULT_HEIGHT),
            action=login,
            text='ENTER WORLD',
            font=FONT_ALICE_IN_WONDERLAND_18
        )

        create_account_button = Button(
            self.game_surface,
            center_x=(self.game_surface.get_width() // 2),
            center_y=(5 * self.game_surface.get_height() // 8) + (5 * InputBox.DEFAULT_HEIGHT),
            action=login,
            text='CREATE ACCOUNT',
            font=FONT_ALICE_IN_WONDERLAND_18
        )

        login_screen_buttons = [
            quit_button,
            login_button,
            create_account_button
        ]

        copyright_message_line_1 = FONT_ARIAL_18.render(
            f'© 2025 {_PROJECT_NAME}. All rights reserved.',
            False,
            WHITE
        )

        copyright_message_line_2 = FONT_ARIAL_18.render(
            f'Version: {_VERSION}',
            False,
            WHITE
        )

        self.sound_manager.play_login_screen_soundtrack()

        account_name_text_box.set_text('jakub')
        password_text_box.set_text('12345')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                for input_box in input_boxes:
                    input_box.handle_events(event)

            self.game_surface.fill(BLACK)
            self.game_surface.blit(start_screen_image, start_screen_image_position)
            self.game_surface.blit(name_image, name_image_position)
            self.game_surface.blit(
                copyright_message_line_1,
                (
                    self.game_surface.get_width() // 2 - copyright_message_line_1.get_width() // 2,
                    self.game_surface.get_height() - 60
                )
            )
            self.game_surface.blit(
                copyright_message_line_2,
                (
                    self.game_surface.get_width() // 2 - copyright_message_line_2.get_width() // 2,
                    self.game_surface.get_height() - 40
                )
            )

            for input_box in input_boxes:
                input_box.draw()

            for login_screen_button in login_screen_buttons:
                login_screen_button.draw()

            for login_screen_button in login_screen_buttons:
                login_screen_button.handle_event()

            if pygame.key.get_pressed()[pygame.K_RETURN] or login_button.handle_event():
                if login():
                    self.screen_manager.next_screen = ScreenType.GAME
                    return

            self.mouse_manager.draw_cursor(CursorType.POINT)

            self.screen_surface.blit(self.game_surface, (0, 0))
            pygame.display.flip()

            self.game_clock.tick()
