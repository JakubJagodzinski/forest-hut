from database.game_database_table_columns_names import ItemsTable, CharacterEquipmentTable, EquipmentSlotsTable
from src.enums.error_message_type import ErrorMessageType
from src.interface.item_tiles_grid import ItemTilesGrid
from src.interface.window import Window
from src.database_service import DatabaseService


class EquipmentManager(Window):
    _instance = None

    Y = 300
    WINDOW_OFFSET_X = 10
    WIDTH = 400
    HEIGHT = 400

    EQUIPMENT_TILES_GRID_OFFSET_X = 5
    EQUIPMENT_TILES_GRID_OFFSET_Y = 5

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

            super().__init__(
                game_surface,
                x=game_surface.get_width() - self.WIDTH - self.WINDOW_OFFSET_X,
                y=self.Y,
                width=self.WIDTH,
                height=self.HEIGHT,
                name='EQUIPMENT'
            )

            self.player_manager = None
            self.item_icons_manager = None
            self.sound_manager = None
            self.error_messages_manager = None

            self.character_id = character_id

            self.equipped_items = self.create_equipment_dict()

            self.equipment_item_tiles_grid = ItemTilesGrid(
                self.game_surface,
                self.content_rect.x + self.EQUIPMENT_TILES_GRID_OFFSET_X,
                self.content_rect.y + self.EQUIPMENT_TILES_GRID_OFFSET_Y,
                len(self.equipped_items),
                1
            )

            equipment_slots = DatabaseService.get_equipment_slots()
            for equipment_slot in equipment_slots:
                slot_id = equipment_slot[EquipmentSlotsTable.EQUIPMENT_SLOT_ID]
                slot_name = equipment_slot[EquipmentSlotsTable.EQUIPMENT_SLOT_NAME]
                self.equipment_item_tiles_grid.set_tile_name(slot_id - 1, 0, slot_name)
            self.set_items()

    def setup_references(self):
        from src.managers.ui.error_messages_manager import ErrorMessagesManager
        from src.managers.ui.item_icons_manager import ItemIconsManager
        from src.managers.core.sound_manager import SoundManager
        from src.managers.gameplay.player_manager import PlayerManager

        self.player_manager = PlayerManager.get_instance()
        self.item_icons_manager = ItemIconsManager.get_instance()
        self.sound_manager = SoundManager.get_instance()
        self.error_messages_manager = ErrorMessagesManager.get_instance()

    def create_equipment_dict(self):
        character_equipped_items = DatabaseService.get_character_equipped_items(self.character_id)

        item_ids = [equipped_item[CharacterEquipmentTable.ITEM_ID] for equipped_item in character_equipped_items]
        items = DatabaseService.get_items(item_ids)

        equipment_dict = {}
        equipment_slots = DatabaseService.get_equipment_slots()
        for equipment_slot in equipment_slots:
            equipment_dict[equipment_slot[EquipmentSlotsTable.EQUIPMENT_SLOT_ID]] = None

        for character_equipped_item in character_equipped_items:
            item_id = character_equipped_item[CharacterEquipmentTable.ITEM_ID]
            item_info = None

            for item_info in items:
                if item_info[ItemsTable.ITEM_ID] == item_id:
                    item_info = item_info
                    break

            slot_id = character_equipped_item[CharacterEquipmentTable.EQUIPMENT_SLOT_ID]
            equipment_dict[slot_id] = item_info

        return equipment_dict

    def can_item_be_equipped(self, item_info):
        if self.player_manager.is_dead:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.YOU_ARE_DEAD)
            return False

        if self.player_manager.is_in_combat:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.YOU_ARE_IN_COMBAT)
            return False

        if item_info[ItemsTable.EQUIPMENT_SLOT_ID] is None:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.CANT_EQUIP_THAT)
            return False

        if self.player_manager.lvl < item_info[ItemsTable.REQUIRED_LVL]:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.YOUR_LVL_IS_TOO_LOW)
            return False

        return True

    def get_slot_item_tile_nr(self, wanted_slot):
        for slot_nr, slot in enumerate(self.equipped_items):
            if slot == wanted_slot:
                return slot_nr

    def set_items(self):
        for slot_id, item_info in self.equipped_items.items():
            self.equipment_item_tiles_grid.set_tile_item(slot_id - 1, 0, item_info, 1)

    def equip_item(self, item_info) -> [str, int]:
        if self.can_item_be_equipped(item_info):
            slot = item_info[ItemsTable.EQUIPMENT_SLOT_ID]
            self.equipment_item_tiles_grid.set_tile_item(self.get_slot_item_tile_nr(slot), 0, item_info, 1)
            taken_off_item_info = self.equipped_items[slot]
            self.equipped_items[slot] = item_info
            return taken_off_item_info
        else:
            return item_info

    def get_left_clicked_slot_name(self):
        clicked_tile_nr = self.equipment_item_tiles_grid.get_left_clicked_tile_nr()
        if clicked_tile_nr is not None:
            slot_name = self.equipment_item_tiles_grid.get_tile_name(clicked_tile_nr, 0)
            return slot_name

    def draw_equipment(self) -> None:
        if self.is_open:
            super().draw()
            self.equipment_item_tiles_grid.draw()

    def draw_hovered(self) -> None:
        if self.is_hovered:
            self.equipment_item_tiles_grid.draw_hovered()
