import pygame

from src.colors import PURPLE, GREEN, BLUE, RED, GRAY_GREEN, BLACK, WHITE, GRAY
from src.common_utils import quit_game, get_fps_rate
from src.enums.character_attribute_type import CharacterAttributeType
from src.fonts import FONT_ALICE_IN_WONDERLAND_16, FONT_MONOSPACE_COURIER_16, \
    FONT_ALICE_IN_WONDERLAND_18, FONT_ALICE_IN_WONDERLAND_36
from src.interface.bar import Bar
from src.interface.button import Button
from src.interface.death_screen import DeathScreen
from src.interface.interface_constants import LOWER_UI_BAR_HEIGHT, OPEN_MENU_BUTTON_OFFSET_X, BORDER_WIDTH, \
    XP_BAR_HEIGHT, MINI_BARS_HEIGHT, MINI_BARS_X, \
    MINI_BARS_WIDTH, MINI_BARS_PARTS, XP_BAR_PARTS
from src.interface.label import Label
from src.interface.menu_window import MenuWindow
from src.keybindings import KEY_SWITCH_SHOW_INTERFACE, KEY_SWITCH_SHOW_FPS_RATE, KEY_USE_MANA_POTION, KEY_USE_HP_POTION, \
    KEY_SWITCH_OPEN_INVENTORY, KEY_SWITCH_OPEN_EQUIPMENT, KEY_SWITCH_SHOW_LOOT_NAMES, \
    KEY_SWITCH_SHOW_HOSTILE_NPC_MINI_HP_BARS, \
    KEY_SWITCH_SHOW_FRIENDLY_NPC_MINI_HP_BARS, KEY_SWITCH_OPEN_CHAT, KEY_SWITCH_OPEN_CHAT_INPUT_BOX
from src.paths import PATH_IMAGE_INVENTORY, PATH_IMAGE_EQUIPMENT, PATH_IMAGE_TOWN_PORTAL, PATH_IMAGE_SUN, \
    PATH_IMAGE_MOON
from src.renderers.kill_series_renderer import KillSeriesRenderer


class InterfaceManager:
    _instance = None

    LOCATION_NAME_Y = 15
    LOCATION_NAME_PADDING_X = 5

    MINI_MAP_RADIUS = 50
    MINI_MAP_OFFSET_X = 10
    MINI_MAP_OFFSET_Y = 10
    PLAYER_INDICATOR_RADIUS = 2

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_surface, account_name):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            self.game_surface = game_surface
            self._account_name = account_name

            self.game_clock = None
            self.datetime_manager = None
            self.map_manager = None
            self.player_manager = None
            self.inventory_manager = None
            self.equipment_manager = None
            self.chat_manager = None
            self.npcs_manager = None
            self.sound_manager = None
            self.potions_manager = None
            self.error_messages_manager = None
            self.loot_manager = None
            self.vendor_manager = None
            self.conversation_manager = None
            self.kill_series_manager = None
            self.choice_window = None
            self.kill_series_renderer = KillSeriesRenderer(game_surface)

            self.death_screen = None

            self._is_game_over = False
            self._quit_to_desktop = False

            self._is_interface_visible = True
            self._is_fps_rate_visible = False

            self.fps_rate_y = self.game_surface.get_height() - (LOWER_UI_BAR_HEIGHT // 2)

            self.location_name_font = FONT_ALICE_IN_WONDERLAND_16

            self.lower_ui_bar_rect = pygame.Rect(
                0,
                self.game_surface.get_height() - LOWER_UI_BAR_HEIGHT,
                self.game_surface.get_width(),
                LOWER_UI_BAR_HEIGHT
            )

            self.xp_bar = Bar(
                game_surface=self.game_surface,
                x=0,
                y=(self.game_surface.get_height()
                   - LOWER_UI_BAR_HEIGHT
                   - XP_BAR_HEIGHT),
                width=self.game_surface.get_width(),
                height=XP_BAR_HEIGHT,
                color=PURPLE,
                parts=XP_BAR_PARTS,
                text='experience'
            )

            mini_bars_y = (self.game_surface.get_height()
                           - (LOWER_UI_BAR_HEIGHT // 2)
                           - ((3 * MINI_BARS_HEIGHT) // 2))

            self.hp_bar = Bar(
                game_surface=self.game_surface,
                x=MINI_BARS_X,
                y=mini_bars_y,
                width=MINI_BARS_WIDTH,
                height=MINI_BARS_HEIGHT,
                color=RED,
                parts=MINI_BARS_PARTS,
                text='health'
            )

            mana_bar_y = mini_bars_y + MINI_BARS_HEIGHT
            self.mana_bar = Bar(
                game_surface=self.game_surface,
                x=MINI_BARS_X,
                y=mana_bar_y,
                width=MINI_BARS_WIDTH,
                height=MINI_BARS_HEIGHT,
                color=BLUE,
                parts=MINI_BARS_PARTS,
                text='mana'
            )

            stamina_bar_y = mana_bar_y + MINI_BARS_HEIGHT
            self.stamina_bar = Bar(
                game_surface=self.game_surface,
                x=MINI_BARS_X,
                y=stamina_bar_y,
                width=MINI_BARS_WIDTH,
                height=MINI_BARS_HEIGHT,
                color=GREEN,
                parts=MINI_BARS_PARTS,
                text='stamina'
            )

            self.buttons = []

            lower_ui_bar_middle_y = self.game_surface.get_height() - (LOWER_UI_BAR_HEIGHT // 2)

            self.menu_window = MenuWindow(game_surface, self)
            self.open_menu_button = Button(
                game_surface=game_surface,
                center_x=game_surface.get_width() - OPEN_MENU_BUTTON_OFFSET_X,
                center_y=lower_ui_bar_middle_y,
                button_color=GRAY_GREEN,
                text_color=BLACK,
                font=FONT_ALICE_IN_WONDERLAND_18,
                action=self.menu_window.switch_open,
                text='MENU',
                with_border=True
            )

            self.level_font = FONT_ALICE_IN_WONDERLAND_36
            self.level_text = None
            self.level_text_draw_x = None
            self.level_text_draw_y = None

            self.location_name_text = None
            self.location_name_label = None
            self.location_name_x = None

            self.ICON_SIZE = 25
            self.ICON_X = 10
            self.ICON_Y = 10

            self.DATETIME_LABEL_WIDTH = 250
            self.DATETIME_LABEL_HEIGHT = 20
            self.DATETIME_TEXT_PADDING_X = 5

            self.font = FONT_ALICE_IN_WONDERLAND_18

            self.sun_icon = pygame.image.load(PATH_IMAGE_SUN).convert_alpha()
            self.sun_icon = pygame.transform.scale(self.sun_icon, (self.ICON_SIZE, self.ICON_SIZE))

            self.moon_icon = pygame.image.load(PATH_IMAGE_MOON).convert_alpha()
            self.moon_icon = pygame.transform.scale(self.moon_icon, (self.ICON_SIZE, self.ICON_SIZE))

            self.icon_rect = pygame.Rect(
                self.ICON_X,
                self.ICON_Y,
                self.ICON_SIZE,
                self.ICON_SIZE,
            )

            self.datetime_x = (self.ICON_X
                               + self.sun_icon.get_width()
                               + (self.sun_icon.get_width() // 2))
            self.datetime_y = (self.ICON_Y
                               + (self.sun_icon.get_height() // 2)
                               - (self.font.get_height() // 2))

            self.datetime_label = Label(
                game_surface=self.game_surface,
                x=self.datetime_x,
                y=self.datetime_y,
                width=self.DATETIME_LABEL_WIDTH,
                height=self.DATETIME_LABEL_HEIGHT,
                background_color=GRAY_GREEN,
                border_color=BLACK
            )

            self.datetime_text = None

            self.mini_map_x = (self.game_surface.get_width()
                               - self.MINI_MAP_OFFSET_X
                               - self.MINI_MAP_RADIUS)
            self.mini_map_y = (self.LOCATION_NAME_Y
                               + self.location_name_font.get_height()
                               + self.MINI_MAP_OFFSET_Y
                               + self.MINI_MAP_RADIUS)

            self.player_immune_screen_overlay = pygame.Surface(
                (
                    self.game_surface.get_width(),
                    self.game_surface.get_height()
                )
            )
            self.player_immune_screen_overlay.fill(WHITE)
            self.player_immune_screen_overlay.set_alpha(110)

    def setup_references(self):
        from src.managers.ui.chat_manager import ChatManager
        from src.managers.gameplay.conversation_manager import ConversationManager
        from src.managers.gameplay.datetime_manager import DatetimeManager
        from src.managers.gameplay.equipment_manager import EquipmentManager
        from src.managers.ui.error_messages_manager import ErrorMessagesManager
        from src.managers.gameplay.inventory_manager import InventoryManager
        from src.managers.gameplay.loot_manager import LootManager
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.gameplay.npcs_manager import NpcsManager
        from src.managers.gameplay.player_manager import PlayerManager
        from src.managers.gameplay.potions_manager import PotionsManager
        from src.managers.core.sound_manager import SoundManager
        from src.managers.gameplay.vendor_manager import VendorManager
        from src.game_clock import GameClock
        from src.interface.choice_window import ChoiceWindow

        self.choice_window = ChoiceWindow.get_instance()
        self.game_clock = GameClock.get_instance()
        self.datetime_manager = DatetimeManager.get_instance()
        self.map_manager = MapManager.get_instance()
        self.player_manager = PlayerManager.get_instance()
        self.inventory_manager = InventoryManager.get_instance()
        self.equipment_manager = EquipmentManager.get_instance()
        self.chat_manager = ChatManager.get_instance()
        self.npcs_manager = NpcsManager.get_instance()
        self.sound_manager = SoundManager.get_instance()
        self.potions_manager = PotionsManager.get_instance()
        self.error_messages_manager = ErrorMessagesManager.get_instance()
        self.loot_manager = LootManager.get_instance()
        self.vendor_manager = VendorManager.get_instance()
        self.conversation_manager = ConversationManager.get_instance()
        self.kill_series_renderer.setup_references()

    def set_data(self):
        OPEN_BUTTON_SIZE = 40
        OPEN_BUTTON_OFFSET_X = 100
        LOWER_UI_BAR_BUTTONS_OFFSET = 25
        lower_ui_bar_middle_y = self.game_surface.get_height() - (LOWER_UI_BAR_HEIGHT // 2)

        inventory_open_button_image = pygame.image.load(PATH_IMAGE_INVENTORY).convert_alpha()
        inventory_open_button_image = pygame.transform.scale(
            inventory_open_button_image,
            (OPEN_BUTTON_SIZE, OPEN_BUTTON_SIZE)
        )

        backpack_button = Button(
            game_surface=self.game_surface,
            center_x=self.game_surface.get_width() - OPEN_BUTTON_OFFSET_X,
            center_y=lower_ui_bar_middle_y,
            image=inventory_open_button_image,
            action=self.inventory_manager.switch_open
        )
        self.buttons.append(backpack_button)

        equipment_open_button_image = pygame.image.load(PATH_IMAGE_EQUIPMENT).convert_alpha()
        equipment_open_button_image = pygame.transform.scale(
            equipment_open_button_image,
            (OPEN_BUTTON_SIZE, OPEN_BUTTON_SIZE)
        )

        equipment_button = Button(
            game_surface=self.game_surface,
            center_x=(self.game_surface.get_width()
                      - OPEN_BUTTON_OFFSET_X
                      - OPEN_BUTTON_SIZE
                      - LOWER_UI_BAR_BUTTONS_OFFSET),
            center_y=lower_ui_bar_middle_y,
            image=equipment_open_button_image,
            action=self.equipment_manager.switch_open
        )
        self.buttons.append(equipment_button)

        town_portal_open_button_image = pygame.image.load(PATH_IMAGE_TOWN_PORTAL).convert_alpha()
        town_portal_open_button_image = pygame.transform.scale(
            town_portal_open_button_image,
            (OPEN_BUTTON_SIZE, OPEN_BUTTON_SIZE)
        )

        town_portal_button = Button(
            game_surface=self.game_surface,
            center_x=(self.game_surface.get_width()
                      - OPEN_BUTTON_OFFSET_X
                      - (2 * (OPEN_BUTTON_SIZE + LOWER_UI_BAR_BUTTONS_OFFSET))),
            center_y=lower_ui_bar_middle_y,
            image=town_portal_open_button_image,
            action=self.player_manager.open_portal_to_town_spell.begin_cast
        )
        self.buttons.append(town_portal_button)

        self.death_screen = DeathScreen(
            self.game_surface,
            self.player_manager.is_hardcore,
            self.player_manager.resurrect_here,
            self.player_manager.resurrect_in_town,
            self.delete_character
        )

    def switch_show_interface(self) -> None:
        self._is_interface_visible = not self._is_interface_visible

    def switch_show_fps_rate(self):
        self._is_fps_rate_visible = not self._is_fps_rate_visible

    def save_game(self) -> None:
        # TODO add autosave
        pass

    def open_choice_window(self, message, callback):
        if not self.choice_window.is_open:
            self.choice_window.open(message, callback)

    def handle_events(self) -> [bool, bool]:
        handled_keyboard, handled_mouse, hovered = False, False, False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.handle_mouse_events(event):
                    handled_mouse = True
            if event.type == pygame.KEYDOWN:
                if self.handle_keyboard_events(event):
                    handled_keyboard = True
        if self.is_hovered:
            hovered = True
            handled_mouse = True
        return handled_keyboard, handled_mouse, hovered

    def handle_mouse_events(self, event) -> bool:
        if self._is_interface_visible:
            if self.player_manager.is_dead and self.death_screen.handle_mouse_events():
                return True
            if self.choice_window.handle_mouse_events():
                return True
            if self.open_menu_button.handle_event():
                return True

            if self.game_clock.is_game_paused:
                if self.menu_window.handle_mouse_events(event):
                    return True
            else:
                if self.vendor_manager.handle_mouse_events(event):
                    return True
                if self.chat_manager.handle_mouse_events(event):
                    return True
                if self.equipment_manager.handle_mouse_events(event):
                    return True
                if self.inventory_manager.handle_mouse_events(event):
                    return True
                if self.potions_manager.handle_mouse_events():
                    return True
                for interface_button in self.buttons:
                    if interface_button.handle_event():
                        return True

        return False

    def handle_keyboard_events(self, event) -> bool:
        keys = pygame.key.get_pressed()

        if self.choice_window.is_open:
            if keys[pygame.K_ESCAPE]:
                self.choice_window.close()
                return True

        if self.chat_manager.handle_keyboard_events(event):
            return True

        if keys[KEY_SWITCH_SHOW_INTERFACE]:
            self.switch_show_interface()
            return True

        if keys[KEY_SWITCH_SHOW_FPS_RATE]:
            self.switch_show_fps_rate()
            return True

        if not self._is_interface_visible:
            if keys[pygame.K_ESCAPE]:
                self.switch_show_interface()
                return True
        else:
            if self.game_clock.is_game_paused:
                if keys[pygame.K_ESCAPE]:
                    if self.menu_window.whatsnew_window.is_open:
                        self.menu_window.whatsnew_window.close()
                        return True
                    if self.menu_window.controls_window.is_open:
                        self.menu_window.controls_window.close()
                        return True
                    self.menu_window.switch_open()
                    return True
            else:
                if keys[pygame.K_ESCAPE]:
                    if self.inventory_manager.is_any_item_held:
                        self.inventory_manager.put_held_item_back_to_inventory()
                    elif self.vendor_manager.is_open:
                        self.vendor_manager.close()
                    elif self.equipment_manager.is_open:
                        self.equipment_manager.close()
                    elif self.inventory_manager.is_open:
                        self.inventory_manager.close()
                    else:
                        self.menu_window.switch_open()
                    return True

                if keys[KEY_USE_HP_POTION]:
                    self.potions_manager.use_hp_potion()
                    return True

                if keys[KEY_USE_MANA_POTION]:
                    self.potions_manager.use_mana_potion()
                    return True

                if keys[KEY_SWITCH_OPEN_INVENTORY]:
                    self.inventory_manager.switch_open()
                    return True

                if keys[KEY_SWITCH_OPEN_EQUIPMENT]:
                    self.equipment_manager.switch_open()
                    return True

                if keys[KEY_SWITCH_SHOW_LOOT_NAMES]:
                    self.loot_manager.switch_show_names()

                if keys[KEY_SWITCH_SHOW_HOSTILE_NPC_MINI_HP_BARS]:
                    self.npcs_manager.switch_show_hostile_npc_mini_hp_bars()
                    return True

                if keys[KEY_SWITCH_SHOW_FRIENDLY_NPC_MINI_HP_BARS]:
                    self.npcs_manager.switch_show_friendly_npc_mini_hp_bars()
                    return True

                if keys[KEY_SWITCH_OPEN_CHAT]:
                    self.chat_manager.switch_open()
                    return True

                if self.chat_manager.is_open:
                    if keys[KEY_SWITCH_OPEN_CHAT_INPUT_BOX]:
                        self.chat_manager.switch_open_input_box()
                        return True

        return False

    def delete_character(self):
        from src.database_service import DatabaseService

        DatabaseService.delete_character(self.player_manager.character_id)
        self.quit_game()

    def quit_game(self):
        self.save_game()
        self._is_game_over = True

    def quit_to_desktop(self):
        self.quit_game()
        self._quit_to_desktop = True

    @property
    def is_quit_to_desktop(self):
        return self._quit_to_desktop

    def set_level_text(self):
        self.level_text = self.level_font.render(str(self.player_manager.lvl), False, WHITE)
        self.level_text_draw_x = (MINI_BARS_X
                                  - self.level_text.get_width()
                                  - ((MINI_BARS_X - self.level_text.get_width()) // 2))
        self.level_text_draw_y = (self.game_surface.get_height()
                                  - (LOWER_UI_BAR_HEIGHT // 2)
                                  - (self.level_text.get_height() // 2))

    def set_location_name_text(self):
        self.location_name_text = self.location_name_font.render(
            self.map_manager.get_location_name_with_levels(),
            False,
            BLACK
        )

        self.location_name_x = (self.game_surface.get_width()
                                - self.location_name_text.get_width()
                                - self.LOCATION_NAME_PADDING_X)

        self.location_name_label = Label(
            game_surface=self.game_surface,
            x=self.location_name_x,
            y=self.LOCATION_NAME_Y,
            width=self.location_name_text.get_width() + (2 * self.LOCATION_NAME_PADDING_X),
            height=self.location_name_text.get_height(),
            background_color=GRAY_GREEN,
            border_color=BLACK
        )

    @property
    def is_game_over(self):
        return self._is_game_over

    @property
    def _is_lower_ui_bar_hovered(self):
        return self.lower_ui_bar_rect.collidepoint(pygame.mouse.get_pos())

    @property
    def is_datetime_hovered(self) -> bool:
        return self.icon_rect.collidepoint(pygame.mouse.get_pos()) or self.datetime_label.is_hovered

    @property
    def is_hovered(self) -> bool:
        hovered_results = [
            self._is_lower_ui_bar_hovered,
            self.chat_manager.is_hovered,
            self.equipment_manager.is_hovered,
            self.inventory_manager.is_hovered,
            self.is_datetime_hovered,
            self.xp_bar.is_hovered,
            self.vendor_manager.is_hovered
        ]
        return any(hovered_results)

    def _draw_lower_ui_bar(self) -> None:
        pygame.draw.rect(
            self.game_surface,
            GRAY,
            (
                0,
                self.game_surface.get_height() - LOWER_UI_BAR_HEIGHT,
                self.game_surface.get_width(),
                LOWER_UI_BAR_HEIGHT
            )
        )

    def _draw_buttons(self) -> None:
        for ui_button in self.buttons:
            ui_button.draw()

    def draw_location_name(self) -> None:
        self.location_name_label.draw()

        # draw location name
        self.game_surface.blit(
            self.location_name_text,
            (
                self.location_name_x + self.LOCATION_NAME_PADDING_X,
                self.LOCATION_NAME_Y
            )
        )

    def draw_mini_map(self):
        mini_map = self.map_manager.get_mini_map_circle(self.MINI_MAP_RADIUS)
        if mini_map is not None:
            self.game_surface.blit(
                mini_map,
                (
                    self.mini_map_x - self.MINI_MAP_RADIUS,
                    self.mini_map_y - self.MINI_MAP_RADIUS
                )
            )

        pygame.draw.circle(
            self.game_surface,
            WHITE,
            (
                self.mini_map_x,
                self.mini_map_y
            ),
            self.MINI_MAP_RADIUS,
            width=BORDER_WIDTH
        )

        pygame.draw.circle(
            self.game_surface,
            WHITE,
            (
                self.mini_map_x - self.PLAYER_INDICATOR_RADIUS // 2,
                self.mini_map_y - self.PLAYER_INDICATOR_RADIUS // 2
            ),
            self.PLAYER_INDICATOR_RADIUS
        )

    def draw_fps_rate(self, delta_time) -> None:
        if self._is_fps_rate_visible:
            fps_rate_text = FONT_MONOSPACE_COURIER_16.render(f'FPS: {get_fps_rate(delta_time)}', True, WHITE)
            self.game_surface.blit(
                fps_rate_text,
                (
                    (self.game_surface.get_width() // 2) - (fps_rate_text.get_width() // 2),
                    self.fps_rate_y
                )
            )

    def draw_player_immune_screen_overlay(self):
        self.game_surface.blit(self.player_immune_screen_overlay, (0, 0))

    def draw_level(self) -> None:
        self.game_surface.blit(
            self.level_text,
            (
                self.level_text_draw_x,
                self.level_text_draw_y
            )
        )

    def draw_datetime(self):
        if self.datetime_manager.is_day_now:
            icon = self.sun_icon
        else:
            icon = self.moon_icon

        self.game_surface.blit(icon, (self.ICON_X, self.ICON_Y))

        self.datetime_label.draw()
        self.datetime_text = self.font.render(self.datetime_manager.formatted_datetime, False, BLACK)
        self.game_surface.blit(
            self.datetime_text,
            (self.datetime_x + self.DATETIME_TEXT_PADDING_X, self.datetime_y)
        )

    def draw_bars(self):
        self.xp_bar.draw(
            self.player_manager.xp,
            self.player_manager.required_xp
        )
        self.hp_bar.draw(
            self.player_manager.get_attribute(CharacterAttributeType.HP),
            self.player_manager.get_attribute(CharacterAttributeType.MAX_HP)
        )
        self.mana_bar.draw(
            self.player_manager.get_attribute(CharacterAttributeType.MANA),
            self.player_manager.get_attribute(CharacterAttributeType.MAX_MANA)
        )
        self.stamina_bar.draw(
            self.player_manager.get_attribute(CharacterAttributeType.STAMINA),
            self.player_manager.get_attribute(CharacterAttributeType.MAX_STAMINA)
        )

    def draw_interface(self) -> None:
        if self._is_interface_visible:
            if self.player_manager.is_dead:
                self.death_screen.draw()
            if self.player_manager.is_immune:
                self.draw_player_immune_screen_overlay()
            self._draw_lower_ui_bar()
            self._draw_buttons()
            self.draw_datetime()
            self.draw_location_name()
            # self.draw_mini_map()
            self.draw_bars()
            self.potions_manager.draw_potions()
            self.kill_series_renderer.draw()
            self.draw_level()
            self.inventory_manager.draw_inventory()
            self.equipment_manager.draw_equipment()
            self.chat_manager.draw_chat()
            self.error_messages_manager.draw_error_messages()
            self.menu_window.draw()
            self.open_menu_button.draw()
            self.choice_window.draw()
            self.vendor_manager.draw_vendor_window()
            self.conversation_manager.draw()

            if not self.game_clock.is_game_paused:
                self.draw_hovered()

    def draw_bars_hovered(self):
        self.xp_bar.draw_hovered(
            self.player_manager.xp,
            self.player_manager.required_xp
        )
        self.hp_bar.draw_hovered(
            self.player_manager.get_attribute(CharacterAttributeType.HP),
            self.player_manager.get_attribute(CharacterAttributeType.MAX_HP)
        )
        self.mana_bar.draw_hovered(
            self.player_manager.get_attribute(CharacterAttributeType.MANA),
            self.player_manager.get_attribute(CharacterAttributeType.MAX_MANA)
        )
        self.stamina_bar.draw_hovered(
            self.player_manager.get_attribute(CharacterAttributeType.STAMINA),
            self.player_manager.get_attribute(CharacterAttributeType.MAX_STAMINA)
        )

    def draw_hovered(self) -> None:
        if self._is_interface_visible:
            self.draw_bars_hovered()
            self.inventory_manager.draw_hovered()
            self.equipment_manager.draw_hovered()
            self.vendor_manager.draw_hovered()
