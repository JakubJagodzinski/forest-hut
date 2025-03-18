import os

from database.database_config import GAME_DATABASE_NAME
from database.database_connector import DatabaseConnector
from database.game_database_table_columns_names import MapsTable, AttributesTable, ItemCategoriesTable, ItemsTable, \
    ItemAttributesTable, CharactersTable, CharacterAttributesTable, NpcsTable, NpcAttributesTable, NpcRolesTypesTable, \
    NpcRolesTable, MapNpcPositionsTable, ObjectsTable, MapObjectPositionsTable, KillSeriesTitlesTable, \
    CharacterEquipmentTable, CharacterInventoryTable, CharacterInventoryLimitsTable, CharacterBankTable, \
    CharacterBankLimitsTable, CurrenciesTable, CharacterCurrenciesTable, EquipmentSlotsTable, VendorItemsTable, \
    LocationChangersTable, \
    ObjectTypesTable, LootableObjectItems, RaritiesTable, FactionsTable, CharacterPositionsTable, MapFadingWallsTable, \
    MapFadingWallPositionsTable

CHARACTER_NAME_MIN_LENGTH = 2
CHARACTER_NAME_MAX_LENGTH = 15

CHARACTER_INVENTORY_DEFAULT_LIMIT = 40
CHARACTER_BANK_DEFAULT_LIMIT = 40


def create_game_database():
    if os.path.exists(GAME_DATABASE_NAME):
        os.remove(GAME_DATABASE_NAME)

    database_connector = DatabaseConnector(GAME_DATABASE_NAME)
    database_connector.connect()

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {RaritiesTable._TABLE_NAME} (
            {RaritiesTable.RARITY_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {RaritiesTable.RARITY_NAME} TEXT NOT NULL
        )
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {FactionsTable._TABLE_NAME} (
            {FactionsTable.FACTION_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {FactionsTable.FACTION_NAME} TEXT NOT NULL
        )
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {KillSeriesTitlesTable._TABLE_NAME} (
            {KillSeriesTitlesTable.TITLE_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {KillSeriesTitlesTable.TITLE_NAME} TEXT UNIQUE NOT NULL,
            {KillSeriesTitlesTable.MIN_KILLS} INTEGER NOT NULL CHECK({KillSeriesTitlesTable.MIN_KILLS} > 0)
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CurrenciesTable._TABLE_NAME} (
            {CurrenciesTable.CURRENCY_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {CurrenciesTable.CURRENCY_NAME} TEXT UNIQUE NOT NULL,
            {CurrenciesTable.MAX_AMOUNT} INTEGER DEFAULT NULL CHECK ({CurrenciesTable.MAX_AMOUNT} >= 0 OR {CurrenciesTable.MAX_AMOUNT} IS NULL)
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {AttributesTable._TABLE_NAME} (
            {AttributesTable.ATTRIBUTE_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {AttributesTable.ATTRIBUTE_NAME} TEXT UNIQUE NOT NULL
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {EquipmentSlotsTable._TABLE_NAME} (
            {EquipmentSlotsTable.EQUIPMENT_SLOT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {EquipmentSlotsTable.EQUIPMENT_SLOT_NAME} TEXT UNIQUE NOT NULL
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {MapsTable._TABLE_NAME} (
            {MapsTable.MAP_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {MapsTable.MAP_NAME} TEXT NOT NULL,
            {MapsTable.MIN_LVL} INTEGER NOT NULL,
            {MapsTable.MAX_LVL} INTEGER NOT NULL
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {ItemCategoriesTable._TABLE_NAME} (
            {ItemCategoriesTable.CATEGORY_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {ItemCategoriesTable.PARENT_CATEGORY_ID} INTEGER DEFAULT NULL,
            {ItemCategoriesTable.CATEGORY_NAME} TEXT UNIQUE NOT NULL,
            {ItemCategoriesTable.CATEGORY_DESCRIPTION} TEXT DEFAULT NULL,
            FOREIGN KEY ({ItemCategoriesTable.PARENT_CATEGORY_ID}) REFERENCES item_categories({ItemCategoriesTable.CATEGORY_ID})
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {ItemsTable._TABLE_NAME} (
            {ItemsTable.ITEM_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {ItemsTable.CATEGORY_ID} INTEGER NOT NULL,
            {ItemsTable.EQUIPMENT_SLOT_ID} INTEGER DEFAULT NULL,
            {ItemsTable.ICON_NAME} TEXT NOT NULL,
            {ItemsTable.ITEM_NAME} TEXT NOT NULL,
            {ItemsTable.ITEM_DESCRIPTION} TEXT DEFAULT NULL,
            {ItemsTable.RARITY_ID} INTEGER DEFAULT NULL,
            {ItemsTable.REQUIRED_LVL} INTEGER NOT NULL DEFAULT 0 CHECK({ItemsTable.REQUIRED_LVL} >= 0),
            {ItemsTable.STACK_SIZE} INTEGER NOT NULL DEFAULT 1 CHECK ({ItemsTable.STACK_SIZE} >= 1),
            {ItemsTable.ITEM_VALUE} INTEGER NOT NULL DEFAULT 0 CHECK ({ItemsTable.ITEM_VALUE} >= 0),
            FOREIGN KEY ({ItemsTable.CATEGORY_ID}) REFERENCES {ItemCategoriesTable._TABLE_NAME}({ItemCategoriesTable.CATEGORY_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({ItemsTable.EQUIPMENT_SLOT_ID}) REFERENCES {EquipmentSlotsTable._TABLE_NAME}({EquipmentSlotsTable.EQUIPMENT_SLOT_ID}) ON DELETE SET DEFAULT,
            FOREIGN KEY ({ItemsTable.RARITY_ID}) REFERENCES {RaritiesTable._TABLE_NAME}({RaritiesTable.RARITY_ID}) ON DELETE SET DEFAULT
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {ItemAttributesTable._TABLE_NAME} (
            {ItemAttributesTable.ATTRIBUTE_ID} INTEGER NOT NULL,
            {ItemAttributesTable.ITEM_ID} INTEGER NOT NULL,
            {ItemAttributesTable.ATTRIBUTE_VALUE} REAL NOT NULL,
            PRIMARY KEY ({ItemAttributesTable.ATTRIBUTE_ID}, {ItemAttributesTable.ITEM_ID}),
            FOREIGN KEY ({ItemAttributesTable.ATTRIBUTE_ID}) REFERENCES {AttributesTable._TABLE_NAME}({AttributesTable.ATTRIBUTE_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({ItemAttributesTable.ITEM_ID}) REFERENCES {ItemsTable._TABLE_NAME}({ItemsTable.ITEM_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {NpcRolesTypesTable._TABLE_NAME} (
            {NpcRolesTypesTable.NPC_ROLE_TYPE_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {NpcRolesTypesTable.NPC_ROLE_NAME} TEXT UNIQUE NOT NULL,
            {NpcRolesTypesTable.NPC_ROLE_TABLE_NAME} TEXT UNIQUE DEFAULT NULL
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {NpcsTable._TABLE_NAME} (
            {NpcsTable.NPC_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {NpcsTable.NPC_NAME} TEXT NOT NULL,
            {NpcsTable.SPRITE_NAME} TEXT NOT NULL,
            {NpcsTable.RARITY_ID} INTEGER DEFAULT NULL,
            {NpcsTable.FACTION_ID} INTEGER DEFAULT NULL,
            {NpcsTable.LVL} INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY ({NpcsTable.RARITY_ID}) REFERENCES {RaritiesTable._TABLE_NAME}({RaritiesTable.RARITY_ID}) ON DELETE SET DEFAULT,
            FOREIGN KEY ({NpcsTable.FACTION_ID}) REFERENCES {FactionsTable._TABLE_NAME}({FactionsTable.FACTION_ID}) ON DELETE SET DEFAULT
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {NpcRolesTable._TABLE_NAME} (
            {NpcRolesTable.NPC_ID} INTEGER NOT NULL,
            {NpcRolesTable.NPC_ROLE_TYPE_ID} INTEGER NOT NULL,
            PRIMARY KEY ({NpcRolesTable.NPC_ID}, {NpcRolesTable.NPC_ROLE_TYPE_ID}),
            FOREIGN KEY ({NpcRolesTable.NPC_ID}) REFERENCES {NpcsTable._TABLE_NAME}({NpcsTable.NPC_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({NpcRolesTable.NPC_ROLE_TYPE_ID}) REFERENCES {NpcRolesTypesTable._TABLE_NAME}({NpcRolesTypesTable.NPC_ROLE_TYPE_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {NpcAttributesTable._TABLE_NAME} (
            {NpcAttributesTable.NPC_ID} INTEGER NOT NULL,
            {NpcAttributesTable.ATTRIBUTE_ID} INTEGER NOT NULL,
            {NpcAttributesTable.ATTRIBUTE_VALUE} REAL NOT NULL,
            PRIMARY KEY ({NpcAttributesTable.NPC_ID}, {NpcAttributesTable.ATTRIBUTE_ID}),
            FOREIGN KEY ({NpcAttributesTable.NPC_ID}) REFERENCES {NpcsTable._TABLE_NAME}({NpcsTable.NPC_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({NpcAttributesTable.ATTRIBUTE_ID}) REFERENCES {AttributesTable._TABLE_NAME}({AttributesTable.ATTRIBUTE_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {MapNpcPositionsTable._TABLE_NAME} (
            {MapNpcPositionsTable.MAP_NPC_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {MapNpcPositionsTable.MAP_ID} INTEGER NOT NULL,
            {MapNpcPositionsTable.NPC_ID} INTEGER NOT NULL,
            {MapNpcPositionsTable.X} INTEGER NOT NULL,
            {MapNpcPositionsTable.Y} INTEGER NOT NULL,
            FOREIGN KEY ({MapNpcPositionsTable.MAP_ID}) REFERENCES {MapsTable._TABLE_NAME}({MapsTable.MAP_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({MapNpcPositionsTable.NPC_ID}) REFERENCES {NpcsTable._TABLE_NAME}({NpcsTable.NPC_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {ObjectTypesTable._TABLE_NAME} (
            {ObjectTypesTable.OBJECT_TYPE_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {ObjectTypesTable.OBJECT_TYPE_NAME} TEXT UNIQUE NOT NULL,
            {ObjectTypesTable.OBJECT_TYPE_TABLE_NAME} TEXT UNIQUE NOT NULL
        )
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {ObjectsTable._TABLE_NAME} (
            {ObjectsTable.OBJECT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {ObjectsTable.OBJECT_TYPE_ID} INTEGER NOT NULL,
            {ObjectsTable.OBJECT_NAME} TEXT DEFAULT NULL,
            {ObjectsTable.SPRITE_NAME} TEXT DEFAULT NULL,
            FOREIGN KEY ({ObjectsTable.OBJECT_TYPE_ID}) REFERENCES {ObjectTypesTable._TABLE_NAME}({ObjectTypesTable.OBJECT_TYPE_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {LocationChangersTable._TABLE_NAME} (
            {LocationChangersTable.OBJECT_ID} INTEGER PRIMARY KEY,
            {LocationChangersTable.DESTINATION_MAP_ID} INTEGER NOT NULL,
            {LocationChangersTable.DESTINATION_X} INTEGER NOT NULL,
            {LocationChangersTable.DESTINATION_Y} INTEGER NOT NULL,
            FOREIGN KEY ({LocationChangersTable.OBJECT_ID}) REFERENCES {ObjectsTable._TABLE_NAME}({ObjectsTable.OBJECT_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({LocationChangersTable.DESTINATION_MAP_ID}) REFERENCES {MapsTable._TABLE_NAME}({MapsTable.MAP_ID}) ON DELETE CASCADE
        )
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {LootableObjectItems._TABLE_NAME} (
            {LootableObjectItems.OBJECT_ID} INTEGER NOT NULL,
            {LootableObjectItems.ITEM_ID} INTEGER NOT NULL,
            PRIMARY KEY({LootableObjectItems.OBJECT_ID}, {LootableObjectItems.ITEM_ID}),
            FOREIGN KEY({LootableObjectItems.OBJECT_ID}) REFERENCES {ObjectsTable._TABLE_NAME}({ObjectsTable.OBJECT_ID}) ON DELETE CASCADE,
            FOREIGN KEY({LootableObjectItems.ITEM_ID}) REFERENCES {ItemsTable._TABLE_NAME}({ItemsTable.ITEM_ID}) ON DELETE CASCADE
        )
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {MapObjectPositionsTable._TABLE_NAME} (
            {MapObjectPositionsTable.MAP_OBJECT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {MapObjectPositionsTable.MAP_ID} INTEGER NOT NULL,
            {MapObjectPositionsTable.OBJECT_ID} INTEGER NOT NULL,
            {MapObjectPositionsTable.X} INTEGER NOT NULL,
            {MapObjectPositionsTable.Y} INTEGER NOT NULL,
            FOREIGN KEY ({MapObjectPositionsTable.MAP_ID}) REFERENCES {MapsTable._TABLE_NAME}({MapsTable.MAP_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({MapObjectPositionsTable.OBJECT_ID}) REFERENCES {ObjectsTable._TABLE_NAME}({ObjectsTable.OBJECT_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {VendorItemsTable._TABLE_NAME} (
            {VendorItemsTable.VENDOR_ID} INTEGER NOT NULL,
            {VendorItemsTable.ITEM_ID} INTEGER NOT NULL,
            PRIMARY KEY({VendorItemsTable.VENDOR_ID}, {VendorItemsTable.ITEM_ID}),
            FOREIGN KEY({VendorItemsTable.VENDOR_ID}) REFERENCES {NpcsTable._TABLE_NAME}({VendorItemsTable.VENDOR_ID}) ON DELETE CASCADE,
            FOREIGN KEY({VendorItemsTable.ITEM_ID}) REFERENCES {ItemsTable._TABLE_NAME}({ItemsTable.ITEM_ID}) ON DELETE CASCADE
        )
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharactersTable._TABLE_NAME} (
            {CharactersTable.CHARACTER_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {CharactersTable.ACCOUNT_ID} INTEGER NOT NULL,
            {CharactersTable.IS_HARDCORE} INTEGER NOT NULL DEFAULT 0 CHECK ({CharactersTable.IS_HARDCORE} IN (0, 1)),
            {CharactersTable.CHARACTER_NAME} TEXT UNIQUE NOT NULL CHECK (LENGTH({CharactersTable.CHARACTER_NAME}) BETWEEN {CHARACTER_NAME_MIN_LENGTH} AND {CHARACTER_NAME_MAX_LENGTH} AND {CharactersTable.CHARACTER_NAME} GLOB '[A-Za-z]*'),
            {CharactersTable.FACTION_ID} INTEGER DEFAULT NULL,
            {CharactersTable.LVL} INTEGER DEFAULT 1 CHECK ({CharactersTable.LVL} >= 1),
            {CharactersTable.XP} INTEGER DEFAULT 0 CHECK ({CharactersTable.XP} >= 0),
            FOREIGN KEY ({CharactersTable.FACTION_ID}) REFERENCES {FactionsTable._TABLE_NAME}({FactionsTable.FACTION_ID}) ON DELETE SET DEFAULT
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharacterPositionsTable._TABLE_NAME} (
            {CharacterPositionsTable.CHARACTER_ID} INTEGER PRIMARY KEY,
            {CharacterPositionsTable.MAP_ID} INTEGER NOT NULL DEFAULT 0,
            {CharacterPositionsTable.X} INTEGER NOT NULL,
            {CharacterPositionsTable.Y} INTEGER NOT NULL,
            FOREIGN KEY ({CharacterPositionsTable.CHARACTER_ID}) REFERENCES {CharactersTable._TABLE_NAME}({CharactersTable.CHARACTER_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({CharacterPositionsTable.MAP_ID}) REFERENCES {MapsTable._TABLE_NAME}({MapsTable.MAP_ID}) ON DELETE SET DEFAULT
        )
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharacterAttributesTable._TABLE_NAME} (
            {CharacterAttributesTable.CHARACTER_ID} INTEGER NOT NULL,
            {CharacterAttributesTable.ATTRIBUTE_ID} INTEGER NOT NULL,
            {CharacterAttributesTable.ATTRIBUTE_VALUE} REAL NOT NULL,
            PRIMARY KEY ({CharacterAttributesTable.ATTRIBUTE_ID}, {CharacterAttributesTable.CHARACTER_ID}),
            FOREIGN KEY ({CharacterAttributesTable.CHARACTER_ID}) REFERENCES {CharactersTable._TABLE_NAME}({CharactersTable.CHARACTER_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({CharacterAttributesTable.ATTRIBUTE_ID}) REFERENCES {AttributesTable._TABLE_NAME}({AttributesTable.ATTRIBUTE_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharacterEquipmentTable._TABLE_NAME} (
            {CharacterEquipmentTable.CHARACTER_ID} INTEGER NOT NULL,
            {CharacterEquipmentTable.CHARACTER_ID.EQUIPMENT_SLOT_ID} INTEGER NOT NULL,
            {CharacterEquipmentTable.CHARACTER_ID.ITEM_ID} INTEGER NOT NULL,
            PRIMARY KEY({CharacterEquipmentTable.CHARACTER_ID}, {CharacterEquipmentTable.EQUIPMENT_SLOT_ID}),
            FOREIGN KEY({CharacterEquipmentTable.CHARACTER_ID}) REFERENCES {CharactersTable._TABLE_NAME}({CharactersTable.CHARACTER_ID}) ON DELETE CASCADE,
            FOREIGN KEY({CharacterEquipmentTable.EQUIPMENT_SLOT_ID}) REFERENCES {EquipmentSlotsTable._TABLE_NAME}({EquipmentSlotsTable.EQUIPMENT_SLOT_ID}) ON DELETE CASCADE,
            FOREIGN KEY({CharacterEquipmentTable.ITEM_ID}) REFERENCES {ItemsTable._TABLE_NAME}({ItemsTable.ITEM_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharacterInventoryLimitsTable._TABLE_NAME} (
            {CharacterInventoryLimitsTable.CHARACTER_ID} INTEGER PRIMARY KEY,
            {CharacterInventoryLimitsTable.MAX_SLOTS} INTEGER DEFAULT {CHARACTER_INVENTORY_DEFAULT_LIMIT} CHECK ({CharacterInventoryLimitsTable.MAX_SLOTS} >= {CHARACTER_INVENTORY_DEFAULT_LIMIT}),
            FOREIGN KEY ({CharacterInventoryLimitsTable.CHARACTER_ID}) REFERENCES {CharactersTable._TABLE_NAME}({CharactersTable.CHARACTER_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharacterInventoryTable._TABLE_NAME} (
            {CharacterInventoryTable.CHARACTER_ID} INTEGER NOT NULL,
            {CharacterInventoryTable.ITEM_ID} INTEGER NOT NULL,
            {CharacterInventoryTable.ITEM_QUANTITY} INTEGER NOT NULL CHECK ({CharacterInventoryTable.ITEM_QUANTITY} > 0),
            {CharacterInventoryTable.SLOT_NR} INTEGER NOT NULL CHECK ({CharacterInventoryTable.SLOT_NR} >= 0),
            PRIMARY KEY({CharacterInventoryTable.CHARACTER_ID}, {CharacterInventoryTable.SLOT_NR}),
            FOREIGN KEY({CharacterInventoryTable.CHARACTER_ID}) REFERENCES {CharactersTable._TABLE_NAME}({CharactersTable.CHARACTER_ID}) ON DELETE CASCADE,
            FOREIGN KEY({CharacterInventoryTable.ITEM_ID}) REFERENCES {ItemsTable._TABLE_NAME}({ItemsTable.ITEM_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharacterBankLimitsTable._TABLE_NAME} (
            {CharacterBankLimitsTable.CHARACTER_ID} INTEGER PRIMARY KEY,
            {CharacterBankLimitsTable.MAX_SLOTS} INTEGER NOT NULL DEFAULT {CHARACTER_BANK_DEFAULT_LIMIT} CHECK({CharacterBankLimitsTable.MAX_SLOTS} >= {CHARACTER_BANK_DEFAULT_LIMIT}),
            FOREIGN KEY ({CharacterBankLimitsTable.CHARACTER_ID}) REFERENCES {CharactersTable._TABLE_NAME}({CharactersTable.CHARACTER_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharacterBankTable._TABLE_NAME} (
            {CharacterBankTable.CHARACTER_ID} INTEGER NOT NULL,
            {CharacterBankTable.ITEM_ID} INTEGER NOT NULL,
            {CharacterBankTable.SLOT_NR} INTEGER NOT NULL CHECK({CharacterBankTable.SLOT_NR} >= 0),
            PRIMARY KEY({CharacterBankTable.CHARACTER_ID}, {CharacterBankTable.SLOT_NR}),
            FOREIGN KEY({CharacterBankTable.CHARACTER_ID}) REFERENCES {CharactersTable._TABLE_NAME}({CharactersTable.CHARACTER_ID}) ON DELETE CASCADE,
            FOREIGN KEY({CharacterBankTable.ITEM_ID}) REFERENCES {ItemsTable._TABLE_NAME}({ItemsTable.ITEM_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {CharacterCurrenciesTable._TABLE_NAME} (
            {CharacterCurrenciesTable.CHARACTER_ID} INTEGER NOT NULL,
            {CharacterCurrenciesTable.CURRENCY_ID} INTEGER NOT NULL,
            {CharacterCurrenciesTable.AMOUNT} INTEGER DEFAULT 0 CHECK ({CharacterCurrenciesTable.AMOUNT} >= 0),
            PRIMARY KEY ({CharacterCurrenciesTable.CHARACTER_ID}, {CharacterCurrenciesTable.CURRENCY_ID}),
            FOREIGN KEY ({CharacterCurrenciesTable.CHARACTER_ID}) REFERENCES {CharactersTable._TABLE_NAME}({CharactersTable.CHARACTER_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({CharacterCurrenciesTable.CURRENCY_ID}) REFERENCES {CurrenciesTable._TABLE_NAME}({CurrenciesTable.CURRENCY_ID}) ON DELETE CASCADE
        );
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {MapFadingWallsTable._TABLE_NAME} (
            {MapFadingWallsTable.FADING_WALL_ID} INTEGER PRIMARY KEY,
            {MapFadingWallsTable.IMAGE_PATH} TEXT NOT NULL,
            {MapFadingWallsTable.WALL_WIDTH} INTEGER NOT NULL,
            {MapFadingWallsTable.WALL_HEIGHT} INTEGER NOT NULL
        )
        '''
    )

    database_connector.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {MapFadingWallPositionsTable._TABLE_NAME} (
            {MapFadingWallPositionsTable.MAP_FADING_WALL_POSITION_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {MapFadingWallPositionsTable.FADING_WALL_ID} INTEGER NOT NULL,
            {MapFadingWallPositionsTable.MAP_ID} INTEGER NOT NULL,
            {MapFadingWallPositionsTable.X} INTEGER NOT NULL,
            {MapFadingWallPositionsTable.Y} INTEGER NOT NULL,
            FOREIGN KEY ({MapFadingWallPositionsTable.FADING_WALL_ID}) REFERENCES {MapFadingWallPositionsTable._TABLE_NAME}({MapFadingWallsTable.FADING_WALL_ID}) ON DELETE CASCADE,
            FOREIGN KEY ({MapFadingWallPositionsTable.MAP_ID}) REFERENCES {MapFadingWallPositionsTable._TABLE_NAME}({MapsTable.MAP_ID}) ON DELETE CASCADE
        )
        '''
    )

    database_connector.disconnect()


if __name__ == '__main__':
    create_game_database()
    print("Game database created")
