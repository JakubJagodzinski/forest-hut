import os

import pygame

from database.game_database_table_columns_names import CharacterInventoryTable, ItemsTable
from src.colors import WHITE
from src.database_service import DatabaseService
from src.enums.currency_type import CurrencyType
from src.enums.error_message_type import ErrorMessageType
from src.enums.rarity_type import RarityType
from src.fonts import FONT_ALICE_IN_WONDERLAND_18
from src.interface.interface_constants import LOWER_UI_BAR_HEIGHT, XP_BAR_HEIGHT, WINDOW_DEFAULT_STRIPE_HEIGHT, \
    INTERFACE_TILE_SIZE
from src.interface.item_tiles_grid import ItemTilesGrid
from src.interface.window import Window
from src.managers.core.mouse_manager import MouseManager
from src.paths import DIR_ASSETS_CURRENCIES


class InventoryManager(Window):
    _instance = None

    ITEM_TILE_GRID_ROWS = 5
    ITEM_TILE_GRID_COLUMNS = 8

    CURRENT_CATEGORY_INFO_OFFSET_Y = 40

    CURRENCY_ICON_SIZE = 15
    CURRENCY_OFFSET_Y = 40
    GOLD_INFO_OFFSET_X = 10

    ETERNAL_ICE_OFFSET_X = 10

    INVENTORY_WINDOW_OFFSET = 10
    INVENTORY_WINDOW_WIDTH = (ITEM_TILE_GRID_COLUMNS * INTERFACE_TILE_SIZE)
    INVENTORY_WINDOW_HEIGHT = (ITEM_TILE_GRID_ROWS * INTERFACE_TILE_SIZE) + (2 * WINDOW_DEFAULT_STRIPE_HEIGHT)

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_surface, character_id):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            x = (game_surface.get_width()
                 - self.INVENTORY_WINDOW_OFFSET
                 - self.INVENTORY_WINDOW_WIDTH)
            y = (game_surface.get_height()
                 - LOWER_UI_BAR_HEIGHT
                 - XP_BAR_HEIGHT
                 - self.INVENTORY_WINDOW_OFFSET
                 - self.INVENTORY_WINDOW_HEIGHT)
            super().__init__(
                game_surface,
                x,
                y,
                self.INVENTORY_WINDOW_WIDTH,
                self.INVENTORY_WINDOW_HEIGHT,
                name='INVENTORY'
            )

            self.character_id = character_id

            self.loot_manager = None
            self.player_manager = None
            self.error_messages_manager = None
            self.vendor_manager = None
            self.item_icons_manager = None
            self.equipment_manager = None
            self.sound_manager = None

            self.currencies = DatabaseService.get_character_currencies(character_id)
            self.currency_font = FONT_ALICE_IN_WONDERLAND_18
            self.currency_icons = {}

            self.inventory_limits = DatabaseService.get_character_inventory_limits(character_id)

            self.item_tiles_grid = ItemTilesGrid(
                game_surface=self.game_surface,
                x=self.content_rect.x,
                y=self.content_rect.y,
                rows=self.ITEM_TILE_GRID_ROWS,
                columns=self.ITEM_TILE_GRID_COLUMNS,
                max_tiles=self.inventory_limits
            )

            self.inventory = self.create_inventory_dict()

            self.held_item_slot_nr = None
            self.held_item_info = None
            self.held_item_quantity = None

    def setup_references(self):
        from src.managers.gameplay.equipment_manager import EquipmentManager
        from src.managers.ui.error_messages_manager import ErrorMessagesManager
        from src.managers.ui.item_icons_manager import ItemIconsManager
        from src.managers.gameplay.loot_manager import LootManager
        from src.managers.gameplay.vendor_manager import VendorManager
        from src.managers.core.sound_manager import SoundManager
        from src.managers.gameplay.player_manager import PlayerManager

        self.loot_manager = LootManager.get_instance()
        self.error_messages_manager = ErrorMessagesManager.get_instance()
        self.player_manager = PlayerManager.get_instance()
        self.vendor_manager = VendorManager.get_instance()
        self.item_icons_manager = ItemIconsManager.get_instance()
        self.equipment_manager = EquipmentManager.get_instance()
        self.sound_manager = SoundManager.get_instance()

    def set_data(self):
        self.load_currency_icons()

    def create_inventory_dict(self):
        character_inventory = DatabaseService.get_character_inventory(self.character_id)
        item_ids = [inventory_entry[CharacterInventoryTable.ITEM_ID] for inventory_entry in character_inventory]
        items = DatabaseService.get_items(item_ids)
        inventory_dict = {}
        for inventory_entry in character_inventory:
            for item_info in items:
                if item_info[ItemsTable.ITEM_ID] == inventory_entry[CharacterInventoryTable.ITEM_ID]:
                    inventory_dict[inventory_entry[CharacterInventoryTable.SLOT_NR]] = [item_info, inventory_entry[
                        CharacterInventoryTable.ITEM_QUANTITY]]
                    break
        return inventory_dict

    def load_currency_icons(self):
        for currency_name, amount in self.currencies.items():
            currency_icon = pygame.image.load(
                os.path.join(DIR_ASSETS_CURRENCIES, f'{currency_name}.png')
            ).convert_alpha()
            currency_icon = pygame.transform.scale(currency_icon, (self.CURRENCY_ICON_SIZE, self.CURRENCY_ICON_SIZE))
            self.currency_icons[currency_name] = currency_icon

    def get_first_free_slot(self):
        free_slot_nr = 0
        while free_slot_nr in self.inventory and free_slot_nr < self.inventory_limits:
            free_slot_nr += 1
        return free_slot_nr

    def is_slot_occupied(self, slot_nr) -> bool:
        return slot_nr is not None and self.inventory.get(slot_nr, None) is not None

    @property
    def is_inventory_full(self) -> bool:
        return len(self.inventory) >= self.inventory_limits

    def get_currencies(self) -> list:
        return self.currencies

    def sell_all_trash(self):
        total_value = 0
        slots_to_clear = []

        for slot_nr, [item_info, item_quantity] in self.inventory.items():
            if item_info[ItemsTable.RARITY_ID] == RarityType.POOR:
                total_value += (item_quantity * item_info[ItemsTable.ITEM_VALUE])
                self.vendor_manager.add_player_sold_item(item_info, item_quantity)
                slots_to_clear.append(slot_nr)

        self.add_gold(total_value)

        for slot_to_clear in slots_to_clear:
            del self.inventory[slot_to_clear]

    def add_gold(self, amount: int) -> None:
        self.currencies[CurrencyType.GOLD] += amount

    def decrease_currency(self, currency_name, amount: int) -> None:
        self.currencies[currency_name] -= amount

    def get_currency(self, currency_name) -> int:
        return self.currencies[currency_name]

    def set_item_tiles_grid_items(self):
        self.item_tiles_grid.clear()
        for slot_nr, [item_info, item_quantity] in self.inventory.items():
            self.item_tiles_grid.set_item(slot_nr, item_info, item_quantity)

    def add_item_to_inventory(self, item_info, item_quantity, slot_nr=None) -> None:
        if self.is_inventory_full:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.INVENTORY_IS_FULL)
            self.loot_manager.drop_loot(item_info, item_quantity, self.player_manager.position)
        else:
            free_slot_nr = self.get_first_free_slot()
            if slot_nr is None:
                slot_nr = free_slot_nr
            else:
                if self.is_slot_occupied(slot_nr):
                    slot_nr = free_slot_nr
            self.inventory[slot_nr] = [item_info, item_quantity]

    def remove_item_from_inventory(self, slot_nr: int) -> None:
        self.inventory.pop(slot_nr)

    def handle_equip_item(self) -> bool:
        if self.equipment_manager.is_open:
            clicked_slot_nr = self.item_tiles_grid.get_right_clicked_tile_nr()
            if self.is_slot_occupied(clicked_slot_nr):
                clicked_item_info = self.inventory[clicked_slot_nr][0]
                take_off_item_info = self.equipment_manager.equip_item(clicked_item_info)
                self.remove_item_from_inventory(clicked_slot_nr)
                if take_off_item_info is not None:
                    self.add_item_to_inventory(take_off_item_info, 1, clicked_slot_nr)
                return True
        return False

    def sell_item(self, slot_nr):
        item_info, item_quantity = self.inventory[slot_nr]
        self.vendor_manager.add_player_sold_item(item_info, item_quantity)
        self.remove_item_from_inventory(slot_nr)
        total_value = (item_quantity * item_info[ItemsTable.ITEM_VALUE])
        self.add_gold(total_value)

    def handle_sell_item(self) -> bool:
        if self.vendor_manager.is_open:
            clicked_slot_nr = self.item_tiles_grid.get_right_clicked_tile_nr()
            if self.is_slot_occupied(clicked_slot_nr):
                self.sell_item(clicked_slot_nr)
                return True
        return False

    def handle_pick_item_from_inventory(self) -> bool:
        clicked_slot_nr = self.item_tiles_grid.get_left_clicked_tile_nr()
        if self.held_item_info is None and clicked_slot_nr is not None:
            if self.is_slot_occupied(clicked_slot_nr):
                self.held_item_slot_nr = clicked_slot_nr
                self.held_item_info = self.inventory[clicked_slot_nr][0]
                self.held_item_quantity = self.inventory[clicked_slot_nr][1]
                return True
        return False

    def handle_put_held_item_back_to_inventory(self) -> bool:
        clicked_slot_nr = self.item_tiles_grid.get_left_clicked_tile_nr()
        if self.held_item_info is not None and clicked_slot_nr is not None:
            if self.is_slot_occupied(clicked_slot_nr):
                another_item_info = self.inventory[clicked_slot_nr][0]
                another_item_quantity = self.inventory[clicked_slot_nr][1]
                self.inventory[self.held_item_slot_nr][0] = another_item_info
                self.inventory[self.held_item_slot_nr][1] = another_item_quantity
                self.inventory[clicked_slot_nr][0] = self.held_item_info
                self.inventory[clicked_slot_nr][1] = self.held_item_quantity
            else:
                self.inventory[clicked_slot_nr] = [self.held_item_info, self.held_item_quantity]
                self.inventory.pop(self.held_item_slot_nr)
            self.held_item_info = None
            return True
        else:
            return False

    def put_held_item_back_to_inventory(self) -> bool:
        if self.is_any_item_held:
            self.held_item_info = None
            return True
        else:
            return False

    @property
    def is_any_item_held(self) -> bool:
        return self.held_item_info is not None

    def handle_drop_held_item_to_ground(self) -> bool:
        if MouseManager.is_left_clicked() and self.held_item_info is not None:
            self.loot_manager.drop_loot(
                self.held_item_info,
                self.held_item_quantity,
                self.player_manager.position
            )
            self.remove_item_from_inventory(
                self.held_item_slot_nr
            )
            self.held_item_info = None
            return True
        return False

    def handle_equip_held_item(self) -> bool:
        if self.held_item_info is not None and self.equipment_manager.is_open and self.equipment_manager.is_hovered:
            slot_name = self.equipment_manager.get_left_clicked_slot_name()
            if slot_name is not None:
                unequipped_item = self.equipment_manager.equip_item(self.held_item_info)
                self.remove_item_from_inventory(self.held_item_slot_nr)
                if unequipped_item is not None:
                    self.add_item_to_inventory(unequipped_item, 1, self.held_item_slot_nr)
                self.held_item_info = None
            return True
        return False

    def handle_sell_held_item(self):
        if self.held_item_info is not None and self.vendor_manager.is_open and self.vendor_manager.is_hovered:
            self.sell_item(
                self.held_item_slot_nr
            )
            self.held_item_info = None
            return True
        return False

    def handle_mouse_events(self, event=None) -> bool:
        if self.is_open:
            for button in self._buttons:
                if button.handle_event():
                    return True
            if self.handle_sell_item():
                return True
            if self.handle_sell_held_item():
                return True
            if self.handle_equip_item():
                return True
            if self.handle_put_held_item_back_to_inventory():
                return True
            if self.handle_pick_item_from_inventory():
                return True
            if self.handle_equip_held_item():
                return True
            if self.handle_drop_held_item_to_ground():
                return True

        return False

    def draw_currency(self) -> None:
        gold_text = self.currency_font.render(str(self.currencies[CurrencyType.GOLD]), False, WHITE)
        eternal_ice_text = self.currency_font.render(str(self.currencies[CurrencyType.ETERNAL_ICE]), False, WHITE)
        gold_info_x = self.rect.x + self.GOLD_INFO_OFFSET_X
        eternal_ice_info_x = self.rect.x + (self.rect.width // 2) + self.ETERNAL_ICE_OFFSET_X
        currency_icon_y = (self.content_rect.y
                           + self.content_rect.height
                           + (self.stripe_height // 2)
                           - (self.CURRENCY_ICON_SIZE // 2))
        currency_text_y = (self.content_rect.y
                           + self.content_rect.height
                           + (self.stripe_height // 2)
                           - (gold_text.get_height() // 2))
        self.game_surface.blit(self.currency_icons[CurrencyType.GOLD], (gold_info_x, currency_icon_y))
        self.game_surface.blit(self.currency_icons[CurrencyType.ETERNAL_ICE], (eternal_ice_info_x, currency_icon_y))
        self.game_surface.blit(gold_text,
                               (gold_info_x + self.CURRENCY_ICON_SIZE + self.GOLD_INFO_OFFSET_X, currency_text_y))
        self.game_surface.blit(eternal_ice_text,
                               (eternal_ice_info_x + self.CURRENCY_ICON_SIZE + self.ETERNAL_ICE_OFFSET_X,
                                currency_text_y))

    def _draw_buttons(self):
        for inventory_button in self._buttons:
            inventory_button.draw()

    def _draw_inventory_content(self) -> None:
        self.set_item_tiles_grid_items()
        self._draw_buttons()
        self.draw_currency()
        self.item_tiles_grid.draw()

    def draw_held_item(self):
        if self.held_item_info is not None:
            held_item_icon = self.item_icons_manager.get_item_icon(self.held_item_info[ItemsTable.ICON_NAME])
            self.game_surface.blit(held_item_icon, pygame.mouse.get_pos())

    def draw_inventory(self) -> None:
        if self.is_open:
            super().draw()
            self._draw_inventory_content()

    def draw_hovered(self) -> None:
        if self.is_hovered:
            self.item_tiles_grid.draw_hovered()
        self.draw_held_item()
