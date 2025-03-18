from typing import override

import pygame

from project_info import _PROJECT_NAME, _VERSION
from src.colors import BLACK
from src.common_utils import quit_game
from src.entities.character import CHARACTER_DRAW_SIZE, Character
from src.entities.entity import Entity
from src.entities.entity_marker import EntityMarker
from src.entities.npcs.npc import Npc
from src.entities.npcs.npc_roles.vendor import Vendor
from src.enums.chat_message_color_type import ChatMessageColorType
from src.enums.cursor_type import CursorType
from src.enums.screen_type import ScreenType
from src.interface.choice_window import ChoiceWindow
from src.interface.item_tile import ItemTile
from src.interface.menu_window import MenuWindow
from src.managers.core.sound_manager import SoundManager
from src.managers.gameplay.conversation_manager import ConversationManager
from src.managers.gameplay.datetime_manager import DatetimeManager
from src.managers.gameplay.equipment_manager import EquipmentManager
from src.managers.gameplay.interactive_objects_manager import InteractiveObjectsManager
from src.managers.gameplay.inventory_manager import InventoryManager
from src.managers.gameplay.kill_series_manager import KillSeriesManager
from src.managers.gameplay.loot_manager import LootManager
from src.managers.gameplay.map_manager import MapManager
from src.managers.gameplay.npcs_manager import NpcsManager
from src.managers.gameplay.player_manager import PlayerManager
from src.managers.gameplay.potions_manager import PotionsManager
from src.managers.gameplay.quotes_manager import QuotesManager, Quote
from src.managers.gameplay.vendor_manager import VendorManager
from src.managers.ui.chat_manager import ChatManager
from src.managers.ui.command_manager import CommandManager
from src.managers.ui.error_messages_manager import ErrorMessagesManager
from src.managers.ui.interface_manager import InterfaceManager
from src.managers.ui.item_icons_manager import ItemIconsManager
from src.screens.screen import Screen
from src.spells.spell import Spell
from src.sprites.character_sprite import CharacterSprite
from src.sprites.entity_sprite import EntitySprite
from src.sprites.object_sprite import ObjectSprite


class GameScreen(Screen):
    WELCOME_MESSAGE = f'Welcome to {_PROJECT_NAME} version {_VERSION}!'

    def __init__(self):
        super().__init__()

    @override
    def enter(self):
        account_name = self.accounts_manager.get_account_name()
        account_id = self.accounts_manager.get_account_id()

        item_icons_manager = ItemIconsManager()
        ItemTile.setup_references()
        command_manager = CommandManager()
        kill_series_manager = KillSeriesManager(self.game_surface)
        sound_manager = SoundManager()
        error_messages_manager = ErrorMessagesManager(self.game_surface)
        chat_manager = ChatManager(self.game_surface)
        quotes_manager = QuotesManager(self.game_surface)
        equipment_manager = EquipmentManager(self.game_surface, account_id)
        inventory_manager = InventoryManager(self.game_surface, account_id)
        player_manager = PlayerManager(self.game_surface, account_id, account_name)
        map_manager = MapManager(self.game_surface)
        loot_manager = LootManager(self.game_surface)
        datetime_manager = DatetimeManager()
        vendor_manager = VendorManager(self.game_surface)
        conversation_manager = ConversationManager(self.game_surface)
        npcs_manager = NpcsManager(self.game_surface)
        potions_manager = PotionsManager(self.game_surface)
        interface_manager = InterfaceManager(self.game_surface, account_name)
        interactive_objects_manager = InteractiveObjectsManager(self.game_surface)
        choice_window = ChoiceWindow(self.game_surface)

        MenuWindow.setup_references()
        EntitySprite.setup_references()
        Character.setup_references()
        datetime_manager.setup_references()
        Vendor.setup_references()
        Entity.setup_references()
        loot_manager.setup_references()
        player_manager.setup_references()
        potions_manager.setup_references()
        map_manager.setup_references()
        equipment_manager.setup_references()
        inventory_manager.setup_references()
        vendor_manager.setup_references()
        chat_manager.setup_references()
        kill_series_manager.setup_references()
        npcs_manager.setup_references()
        interface_manager.setup_references()
        interactive_objects_manager.setup_references()
        EntityMarker.setup_references()
        Npc.setup_references()
        Spell.setup_references()
        error_messages_manager.setup_references()
        Quote.setup_references()
        ItemTile.setup_references()
        command_manager.setup_references()

        map_manager.load_map(player_manager.map_id)
        datetime_manager.switch_day_night_soundtrack()
        loot_manager.update()
        inventory_manager.set_data()
        EntityMarker.load_entity_markers()
        Npc.initialize_mini_hp_bars(self.game_surface)
        npcs_manager.update()
        CharacterSprite.load_sprites(CHARACTER_DRAW_SIZE)
        ObjectSprite.load_sprites(CHARACTER_DRAW_SIZE)
        command_manager.set_commands()
        interface_manager.set_data()
        interactive_objects_manager.update()
        player_manager.load_spells()
        interface_manager.set_level_text()

        chat_manager.push_message_to_chat(self.WELCOME_MESSAGE, ChatMessageColorType.SYSTEM)
        chat_manager.switch_open()

        while not interface_manager.is_game_over:
            delta_time = self.game_clock.tick()

            cursor_type = CursorType.POINT

            is_keyboard_handled, is_mouse_handled, is_interface_hovered = interface_manager.handle_events()

            if not self.game_clock.is_game_paused:
                if not player_manager.is_dead:

                    player_manager.handle_spell_cast_finish()
                    player_manager.handle_kill_series_end()
                    player_manager.handle_regeneration()
                    player_manager.handle_move(delta_time)

                    if not is_mouse_handled:
                        player_manager.handle_mouse_events()

                    if vendor_manager.is_open and (inventory_manager.is_hovered or vendor_manager.is_hovered):
                        cursor_type = CursorType.SELL
                    if not interface_manager.is_hovered:
                        cursor_type = npcs_manager.get_hovered_npc_info()

                npcs_manager.handle_events()
                npcs_manager.perform_actions(delta_time)
                vendor_manager.handle_auto_close()
                player_manager.handle_death()

                datetime_manager.increment_time(delta_time)

            self.game_surface.fill(BLACK)
            map_manager.draw_map()
            interactive_objects_manager.draw_interactive_objects()
            loot_manager.draw_loot()
            npcs_manager.draw_npcs()
            player_manager.draw_player()
            map_manager.draw_night_overlay()
            if not self.game_clock.is_game_paused:
                npcs_manager.draw_hovered_npc_info()
            quotes_manager.draw_quotes()
            interface_manager.draw_interface()
            interface_manager.draw_fps_rate(delta_time)
            self.mouse_manager.draw_cursor(cursor_type)

            self.screen_surface.blit(self.game_surface, (0, 0))
            pygame.display.flip()

            self.game_clock.update()

        if interface_manager.is_quit_to_desktop:
            quit_game()

        self.screen_manager.next_screen = ScreenType.LOGIN
