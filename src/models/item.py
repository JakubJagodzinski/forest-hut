from database.game_database_table_columns_names import ItemsTable


class Item:

    def __init__(self, item_info, item_quantity, rarities_dict, categories_dict):
        self.id = item_info[ItemsTable.ITEM_ID]
        self.category_name = categories_dict[item_info[ItemsTable.CATEGORY_ID]]
        self.equipment_slot_id = item_info[ItemsTable.EQUIPMENT_SLOT_ID]
        self.icon_name = item_info[ItemsTable.ICON_NAME]
        self.name = item_info[ItemsTable.ITEM_NAME]
        self.description = item_info[ItemsTable.ITEM_DESCRIPTION]
        self.rarity = rarities_dict[item_info[ItemsTable.RARITY_ID]]
        self.required_lvl = item_info[ItemsTable.REQUIRED_LVL]
        self.stack_size = item_info[ItemsTable.STACK_SIZE]
        self.value = item_info[ItemsTable.ITEM_VALUE]
        self.item_quantity = item_quantity
