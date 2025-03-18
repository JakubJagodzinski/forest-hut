from database.game_database_table_columns_names import ItemsTable
from src.colors import WHITE, BLACK
from src.database_service import DatabaseService
from src.enums.error_message_type import ErrorMessageType
from src.fonts import FONT_ALICE_IN_WONDERLAND_18
from src.interface.button import Button
from src.interface.interface_constants import INTERFACE_TILE_SIZE
from src.interface.item_tiles_grid import ItemTilesGrid
from src.interface.window import Window
from src.managers.gameplay.inventory_manager import CurrencyType


class VendorManager(Window):
    _instance = None

    VENDOR_ITEM_TILES_GRID_X = 0
    VENDOR_ITEM_TILES_GRID_Y = 0

    PLAYER_SOLD_ITEM_TILES_GRID_X = 0

    WINDOW_BORDER_OFFSET = 10
    X = WINDOW_BORDER_OFFSET
    Y = WINDOW_BORDER_OFFSET

    TILES_GRID_COLUMNS = 5
    VENDOR_TILES_GRID_ROWS = 4
    PLAYER_TILES_GRID_ROWS = 1

    WINDOW_HEIGHT = (VENDOR_TILES_GRID_ROWS + PLAYER_TILES_GRID_ROWS + 2) * INTERFACE_TILE_SIZE

    PLAYER_SOLD_ITEMS_MAX_SIZE = 20

    player_manager = None
    inventory_manager = None
    error_messages_manager = None
    items_database_manager = None
    loot_manager = None

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

            self.WINDOW_WIDTH = INTERFACE_TILE_SIZE * self.TILES_GRID_COLUMNS

            super().__init__(game_surface, self.X, self.Y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

            self.vendor_reference = None
            self.entity_reference = None

            self.player_sold_items = []

            self.PLAYER_SOLD_ITEM_TILES_GRID_Y = (self.content_rect.y
                                                  + (self.VENDOR_TILES_GRID_ROWS * INTERFACE_TILE_SIZE))

            self.vendor_items_tiles_grid = ItemTilesGrid(
                self.game_surface,
                self.content_rect.x + self.VENDOR_ITEM_TILES_GRID_X,
                self.content_rect.y + self.VENDOR_ITEM_TILES_GRID_Y,
                self.VENDOR_TILES_GRID_ROWS,
                self.TILES_GRID_COLUMNS,
            )

            self.buyback_text = FONT_ALICE_IN_WONDERLAND_18.render('Buyback', False, WHITE)
            self.buyback_x = self.content_rect.x + (self.content_rect.width // 2) - (self.buyback_text.get_width() // 2)
            self.buyback_y = self.content_rect.y + self.PLAYER_SOLD_ITEM_TILES_GRID_Y - self.buyback_text.get_height()

            self.player_sold_items_tiles_grid = ItemTilesGrid(
                self.game_surface,
                self.content_rect.x + self.PLAYER_SOLD_ITEM_TILES_GRID_X,
                self.content_rect.y + self.PLAYER_SOLD_ITEM_TILES_GRID_Y,
                self.PLAYER_TILES_GRID_ROWS,
                self.TILES_GRID_COLUMNS,
            )

    def setup_references(self):
        from src.managers.gameplay.player_manager import PlayerManager
        from src.managers.gameplay.inventory_manager import InventoryManager
        from src.managers.gameplay.loot_manager import LootManager
        from src.managers.ui.item_icons_manager import ItemIconsManager
        from src.managers.ui.error_messages_manager import ErrorMessagesManager

        self.player_manager = PlayerManager.get_instance()
        self.inventory_manager = InventoryManager.get_instance()
        self.error_messages_manager = ErrorMessagesManager.get_instance()
        self.items_database_manager = ItemIconsManager.get_instance()
        self.loot_manager = LootManager.get_instance()

    def set_data(self):
        sell_all_junk_button = Button(
            self.game_surface,
            self.rect.x + (self.WINDOW_WIDTH // 2),
            self.content_rect.y
            + self.content_rect.height
            - (self.content_rect.height
               - (self.PLAYER_SOLD_ITEM_TILES_GRID_Y
                  + (self.PLAYER_TILES_GRID_ROWS * INTERFACE_TILE_SIZE)))
            // 2,
            action=self.inventory_manager.sell_all_trash,
            text='Sell junk',
            button_color=BLACK
        )
        self._buttons.append(sell_all_junk_button)

    def get_latest_player_sold_items(self):
        return self.player_sold_items[:self.grid_size]

    def add_player_sold_item(self, item_info, item_quantity):
        self.player_sold_items.insert(0, [item_info, item_quantity])
        if len(self.player_sold_items) > self.PLAYER_SOLD_ITEMS_MAX_SIZE:
            self.player_sold_items.pop(len(self.player_sold_items) - 1)
        self.player_sold_items_tiles_grid.set_items(self.get_latest_player_sold_items())

    def is_player_sold_item_in_range(self, item_nr) -> bool:
        return 0 <= item_nr < len(self.player_sold_items)

    def is_vendor_item_in_range(self, item_nr) -> bool:
        return 0 <= item_nr < (self.VENDOR_TILES_GRID_ROWS * self.TILES_GRID_COLUMNS)

    def handle_buyback_item(self):
        clicked_slot_nr = self.player_sold_items_tiles_grid.get_right_clicked_tile_nr()
        if clicked_slot_nr is not None and self.is_player_sold_item_in_range(clicked_slot_nr):
            item_info, item_quantity = self.player_sold_items[clicked_slot_nr]
            value = item_quantity * item_info[ItemsTable.ITEM_VALUE]
            if self.inventory_manager.get_currency(CurrencyType.GOLD) < value:
                self.error_messages_manager.push_message_to_queue(
                    ErrorMessageType.NOT_ENOUGH_CURRENCY
                )
            elif self.inventory_manager.is_inventory_full:
                self.error_messages_manager.push_message_to_queue(
                    ErrorMessageType.INVENTORY_IS_FULL
                )
            else:
                self.inventory_manager.decrease_currency(CurrencyType.GOLD, value)
                self.inventory_manager.add_item_to_inventory(item_info, item_quantity)
                self.player_sold_items.pop(clicked_slot_nr)
                self.player_sold_items_tiles_grid.set_items(self.get_latest_player_sold_items())

    def handle_buy_item(self):
        clicked_slot_nr = self.vendor_items_tiles_grid.get_right_clicked_tile_nr()
        if clicked_slot_nr is not None and self.is_vendor_item_in_range(clicked_slot_nr):
            item_info, item_quantity = self.vendor_reference.items[clicked_slot_nr]
            value = item_quantity * item_info[ItemsTable.ITEM_VALUE]
            if self.inventory_manager.get_currency(CurrencyType.GOLD) < value:
                self.error_messages_manager.push_message_to_queue(
                    ErrorMessageType.NOT_ENOUGH_CURRENCY
                )
            elif self.inventory_manager.is_inventory_full:
                self.error_messages_manager.push_message_to_queue(
                    ErrorMessageType.INVENTORY_IS_FULL
                )
            else:
                self.inventory_manager.decrease_currency(CurrencyType.GOLD, value)
                self.inventory_manager.add_item_to_inventory(item_info, item_quantity)
                self.vendor_reference.items.pop(clicked_slot_nr)
                self.vendor_reference.items.append([DatabaseService.get_random_items(1)[0], 1])
                self.vendor_items_tiles_grid.set_items(self.vendor_reference.get_items())

    @property
    def grid_size(self):
        return self.VENDOR_TILES_GRID_ROWS * self.TILES_GRID_COLUMNS

    def handle_mouse_events(self, event=None) -> bool:
        if self.is_open:
            if super().handle_mouse_events(event):
                return True
            if self.handle_buyback_item():
                return True
            if self.handle_buy_item():
                return True
        return False

    def open(self, vendor_reference, entity_reference):
        if self.vendor_reference is None or (
                self.vendor_reference is not None and self.vendor_reference != vendor_reference):
            super().open()
            self.set_name(entity_reference.name)
            self.vendor_reference = vendor_reference
            self.entity_reference = entity_reference
            self.vendor_items_tiles_grid.set_items(vendor_reference.get_items())
            self.inventory_manager.open()

    def close(self):
        super().close()
        self.vendor_reference = None
        self.entity_reference = None

    def handle_auto_close(self):
        if self.vendor_reference is not None:
            if (not self.entity_reference.is_target_in_interaction_distance(self.player_manager)
                    or self.entity_reference.is_dead):
                self.inventory_manager.close()
                self.close()
                return True
        return False

    def draw_vendor_window(self):
        if self.is_open:
            super().draw()
            self.vendor_items_tiles_grid.draw()
            self.game_surface.blit(self.buyback_text, (self.buyback_x, self.buyback_y))
            self.player_sold_items_tiles_grid.draw()

    def draw_hovered(self):
        if self.is_open:
            self.vendor_items_tiles_grid.draw_hovered()
            self.player_sold_items_tiles_grid.draw_hovered()
