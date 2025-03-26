import os

from database.database_connector import DatabaseConnector
from database.game_database_init import GAME_DATABASE_NAME
from database.game_database_table_columns_names import ItemsTable, KillSeriesTitlesTable, NpcsTable, NpcRolesTypesTable, \
    MapsTable, ItemCategoriesTable, AttributesTable, CurrenciesTable, EquipmentSlotsTable, NpcAttributesTable, \
    NpcRolesTable, \
    ObjectTypesTable, ObjectsTable, RaritiesTable, FactionsTable
from src.common_utils import load_json
from src.enums.rarity_type import RarityType
from src.paths import PATH_ITEM_CATEGORIES_JSON, PATH_CURRENCIES_JSON, PATH_MAPS_JSON, \
    PATH_NPC_ROLES_TYPES_JSON, PATH_ATTRIBUTES_JSON, PATH_EQUIPMENT_SLOTS_JSON, \
    PATH_KILL_SERIES_TITLES_JSON, PATH_OBJECT_TYPES_JSON, PATH_RARITIES_JSON, PATH_FACTIONS_JSON, PATH_DIR_ITEMS


def seed_kill_series_titles(database_connector, kill_series_titles):
    kill_series_titles_data = [
        (
            kill_series_title[KillSeriesTitlesTable.TITLE_NAME],
            kill_series_title[KillSeriesTitlesTable.MIN_KILLS]
        )
        for kill_series_title in kill_series_titles
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {KillSeriesTitlesTable._TABLE_NAME} (
            {KillSeriesTitlesTable.TITLE_NAME},
            {KillSeriesTitlesTable.MIN_KILLS}
        ) VALUES (?, ?);
        ''',
        params=kill_series_titles_data
    )


def seed_items(database_connector, items):
    items_data = [
        (
            item[ItemsTable.CATEGORY_ID],
            item[ItemsTable.EQUIPMENT_SLOT_ID],
            os.path.normpath(item[ItemsTable.ICON_NAME]),
            item[ItemsTable.ITEM_NAME],
            item[ItemsTable.ITEM_DESCRIPTION],
            RarityType[item[ItemsTable.RARITY_ID].upper()].value,
            item[ItemsTable.REQUIRED_LVL],
            item[ItemsTable.STACK_SIZE],
            item[ItemsTable.ITEM_VALUE]
        )
        for item in items
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {ItemsTable._TABLE_NAME} (
            {ItemsTable.CATEGORY_ID},
            {ItemsTable.EQUIPMENT_SLOT_ID},
            {ItemsTable.ICON_NAME},
            {ItemsTable.ITEM_NAME},
            {ItemsTable.ITEM_DESCRIPTION},
            {ItemsTable.RARITY_ID},
            {ItemsTable.REQUIRED_LVL},
            {ItemsTable.STACK_SIZE},
            {ItemsTable.ITEM_VALUE}
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''',
        params=items_data
    )


def get_attributes_ids(database_connector):
    database_connector.execute(
        query=f'''
        SELECT *
        FROM {AttributesTable._TABLE_NAME}
        '''
    )

    attributes = database_connector.fetchall()

    return {attribute[AttributesTable.ATTRIBUTE_NAME]: attribute[AttributesTable.ATTRIBUTE_ID] for attribute in
            attributes}


def get_npc_roles_ids(database_connector):
    database_connector.execute(
        query=f'''
        SELECT *
        FROM {NpcRolesTypesTable._TABLE_NAME}
        '''
    )

    return {npc_role_type[NpcRolesTypesTable.NPC_ROLE_NAME]: npc_role_type[NpcRolesTypesTable.NPC_ROLE_TYPE_ID] for
            npc_role_type in
            database_connector.fetchall()}


def seed_npcs(database_connector, npcs):
    attributes_ids = get_attributes_ids(database_connector)

    npc_roles_ids = get_npc_roles_ids(database_connector)

    for npc_data in npcs:
        database_connector.execute(
            query=f'''
            INSERT INTO {NpcsTable._TABLE_NAME} (
                {NpcsTable.NPC_NAME},
                {NpcsTable.SPRITE_NAME},
                {NpcsTable.RARITY_ID},
                {NpcsTable.FACTION_ID},
                {NpcsTable.LVL}
            ) VALUES (?, ?, ?, ?, ?);
            ''',
            params=(
                npc_data[NpcsTable.NPC_NAME],
                npc_data[NpcsTable.SPRITE_NAME],
                npc_data[NpcsTable.RARITY_ID],
                npc_data[NpcsTable.FACTION_ID],
                npc_data[NpcsTable.LVL]
            )
        )

        npc_id = database_connector.lastrowid

        npc_attributes_dict = npc_data[AttributesTable._TABLE_NAME]

        npc_attributes = [(npc_id, attributes_ids[attribute_name], attribute_value) for attribute_name, attribute_value
                          in npc_attributes_dict.items()]

        database_connector.executemany(
            query=f'''
            INSERT INTO {NpcAttributesTable._TABLE_NAME} (
                {NpcAttributesTable.NPC_ID},
                {NpcAttributesTable.ATTRIBUTE_ID},
                {NpcAttributesTable.ATTRIBUTE_VALUE}
            ) VALUES (?, ?, ?);
            ''',
            params=npc_attributes
        )

        npc_roles_names_list = npc_data[NpcRolesTable._TABLE_NAME]

        npc_roles = [(npc_id, npc_roles_ids[role_name]) for role_name in npc_roles_names_list]

        database_connector.executemany(
            query=f'''
            INSERT INTO {NpcRolesTable._TABLE_NAME} (
                {NpcRolesTable.NPC_ID},
                {NpcRolesTable.NPC_ROLE_TYPE_ID}
            ) VALUES (?, ?);
            ''',
            params=npc_roles
        )


def seed_npc_roles_types(database_connector, npc_roles_types):
    npc_roles_types_data = [
        (
            role_name[NpcRolesTypesTable.NPC_ROLE_NAME],
            role_name[NpcRolesTypesTable.NPC_ROLE_TABLE_NAME]
        )
        for role_name in npc_roles_types
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {NpcRolesTypesTable._TABLE_NAME} (
            {NpcRolesTypesTable.NPC_ROLE_NAME},
            {NpcRolesTypesTable.NPC_ROLE_TABLE_NAME}
        ) VALUES (?, ?);
        ''',
        params=npc_roles_types_data
    )


# def put_npcs_on_map(database_connector, map_npc_positions):
#     map_id = database_connector.lastrowid
#
#     map_npc_positions = map_data[MapNpcPositionsTable._TABLE_NAME]
#
#     if len(map_npc_positions) > 0:
#         map_npc_positions_data = [
#             (
#                 map_id,
#                 map_npc_position[MapNpcPositionsTable.NPC_ID],
#                 map_npc_position[MapNpcPositionsTable.X],
#                 map_npc_position[MapNpcPositionsTable.Y]
#             )
#             for map_npc_position in map_npc_positions
#         ]
#
#         database_connector.executemany(
#             f'''
#                    INSERT INTO {MapNpcPositionsTable._TABLE_NAME} (
#                        {MapNpcPositionsTable.MAP_ID},
#                        {MapNpcPositionsTable.NPC_ID},
#                        {MapNpcPositionsTable.X},
#                        {MapNpcPositionsTable.Y}
#                    ) VALUES (?, ?, ?, ?)
#                    ''',
#             map_npc_positions_data
#         )
#
# def put_objects_on_map(database_connector, map_object_positions):
#     map_object_positions = map_data[MapObjectPositionsTable._TABLE_NAME]
#
#     if len(map_object_positions) > 0:
#         map_object_positions_data = [
#             (
#                 map_id,
#                 map_object_position[MapObjectPositionsTable.OBJECT_ID],
#                 map_object_position[MapObjectPositionsTable.X],
#                 map_object_position[MapObjectPositionsTable.Y]
#             )
#             for map_object_position in map_object_positions
#         ]
#
#         database_connector.executemany(
#             f'''
#                                INSERT INTO {MapObjectPositionsTable._TABLE_NAME} (
#                                    {MapObjectPositionsTable.MAP_ID},
#                                    {MapObjectPositionsTable.OBJECT_ID},
#                                    {MapObjectPositionsTable.X},
#                                    {MapObjectPositionsTable.Y}
#                                ) VALUES (?, ?, ?, ?)
#                                ''',
#             map_object_positions_data
#         )

def seed_item_categories(database_connector, item_categories):
    item_categories_data = [
        (
            item_category[ItemCategoriesTable.PARENT_CATEGORY_ID],
            item_category[ItemCategoriesTable.CATEGORY_NAME],
            item_category[ItemCategoriesTable.CATEGORY_DESCRIPTION]
        )
        for item_category in item_categories
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {ItemCategoriesTable._TABLE_NAME} (
            {ItemCategoriesTable.PARENT_CATEGORY_ID},
            {ItemCategoriesTable.CATEGORY_NAME},
            {ItemCategoriesTable.CATEGORY_DESCRIPTION}
        ) VALUES (?, ?, ?)
        ''',
        params=item_categories_data
    )


def seed_maps(database_connector, maps):
    maps_data = [
        (
            map_data[MapsTable.MAP_NAME],
            map_data[MapsTable.MIN_LVL],
            map_data[MapsTable.MAX_LVL]
        )
        for map_data in maps
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {MapsTable._TABLE_NAME} (
            {MapsTable.MAP_NAME},
            {MapsTable.MIN_LVL},
            {MapsTable.MAX_LVL}
        ) VALUES (?, ?, ?)
        ''',
        params=maps_data
    )


def seed_attributes(database_connector, attributes):
    attributes_data = [
        (
            attribute[AttributesTable.ATTRIBUTE_NAME],
        )
        for attribute in attributes
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {AttributesTable._TABLE_NAME} (
            {AttributesTable.ATTRIBUTE_NAME}
        ) VALUES (?)
        ''',
        params=attributes_data
    )


def seed_currencies(database_connector, currencies):
    currencies_data = [
        (
            currency[CurrenciesTable.CURRENCY_NAME],
            currency[CurrenciesTable.MAX_AMOUNT]
        )
        for currency in currencies
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {CurrenciesTable._TABLE_NAME} (
            {CurrenciesTable.CURRENCY_NAME},
            {CurrenciesTable.MAX_AMOUNT}
        ) VALUES (?, ?)
        ''',
        params=currencies_data
    )


def seed_rarities(database_connector, rarities):
    rarities_data = [
        (
            rarity[RaritiesTable.RARITY_NAME],
        )
        for rarity in rarities
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {RaritiesTable._TABLE_NAME} (
            {RaritiesTable.RARITY_NAME}
        ) VALUES (?)
        ''',
        params=rarities_data
    )


def seed_factions(database_connector, factions):
    factions_data = [
        (
            faction[FactionsTable.FACTION_NAME],
        )
        for faction in factions
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {FactionsTable._TABLE_NAME} (
            {FactionsTable.FACTION_NAME}
        ) VALUES (?)
        ''',
        params=factions_data
    )


def seed_equipment_slots(database_connector, equipment_slots):
    equipment_slots_data = [
        (
            equipment_slot[EquipmentSlotsTable.EQUIPMENT_SLOT_NAME],
        )
        for equipment_slot in equipment_slots
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {EquipmentSlotsTable._TABLE_NAME} (
            {EquipmentSlotsTable.EQUIPMENT_SLOT_NAME}
        ) VALUES (?)
        ''',
        params=equipment_slots_data
    )


def seed_object_types(database_connector, object_types):
    object_types_data = [
        (
            object_type[ObjectTypesTable.OBJECT_TYPE_NAME],
            object_type[ObjectTypesTable.OBJECT_TYPE_TABLE_NAME]
        )
        for object_type in object_types
    ]

    database_connector.executemany(
        query=f'''
        INSERT INTO {ObjectTypesTable._TABLE_NAME} (
            {ObjectTypesTable.OBJECT_TYPE_NAME},
            {ObjectTypesTable.OBJECT_TYPE_TABLE_NAME}
        ) VALUES (?, ?);
        ''',
        params=object_types_data
    )


def seed_objects(database_connector, objects):
    for type_objects_data in objects:

        object_type_table_name = type_objects_data[ObjectTypesTable.OBJECT_TYPE_TABLE_NAME]

        database_connector.execute(
            query=f'''
            INSERT INTO {ObjectTypesTable._TABLE_NAME} (
                {ObjectTypesTable.OBJECT_TYPE_NAME},
                {ObjectTypesTable.OBJECT_TYPE_TABLE_NAME}
            ) VALUES (?, ?);
            ''',
            params=(
                type_objects_data[ObjectTypesTable.OBJECT_TYPE_NAME],
                object_type_table_name,
            )
        )

        object_type_id = database_connector.lastrowid

        objects = type_objects_data[ObjectsTable._TABLE_NAME]

        for object_data in objects:
            database_connector.execute(
                query=f'''
                INSERT INTO {ObjectsTable._TABLE_NAME} (
                    {ObjectsTable.OBJECT_TYPE_ID},
                    {ObjectsTable.OBJECT_NAME},
                    {ObjectsTable.SPRITE_NAME}
                ) VALUES (?, ?, ?);
                ''',
                params=(
                    object_type_id,
                    object_data[ObjectsTable.OBJECT_NAME],
                    object_data[ObjectsTable.SPRITE_NAME],
                )
            )

            type_data = object_data['type_data']

            columns = list(type_data.keys())
            values = list(type_data.values())

            database_connector.execute(
                query=f'''
                INSERT INTO {object_type_table_name} (
                    {', '.join(columns)}
                )
                VALUES (
                    {', '.join(['?' for _ in values])}
                );
                ''',
                params=(
                    values,
                )
            )


def main():
    database_connector = DatabaseConnector(GAME_DATABASE_NAME)
    database_connector.connect()

    # --------------------------------DEFINITIONS------------------------------------

    kill_series_titles = load_json(PATH_KILL_SERIES_TITLES_JSON)
    seed_kill_series_titles(database_connector, kill_series_titles)

    attributes = load_json(PATH_ATTRIBUTES_JSON)
    seed_attributes(database_connector, attributes)

    currencies = load_json(PATH_CURRENCIES_JSON)
    seed_currencies(database_connector, currencies)

    rarities = load_json(PATH_RARITIES_JSON)
    seed_rarities(database_connector, rarities)

    factions = load_json(PATH_FACTIONS_JSON)
    seed_factions(database_connector, factions)

    # -------------------------------------- ITEMS ------------------------------------------

    item_categories = load_json(PATH_ITEM_CATEGORIES_JSON)
    seed_item_categories(database_connector, item_categories)

    equipment_slots = load_json(PATH_EQUIPMENT_SLOTS_JSON)
    seed_equipment_slots(database_connector, equipment_slots)

    # ------------------------------------- MAPS -----------------------------------------

    maps = load_json(PATH_MAPS_JSON)
    seed_maps(database_connector, maps)

    # -------------------------------------- NPCS -----------------------------------------

    npc_roles_types = load_json(PATH_NPC_ROLES_TYPES_JSON)
    seed_npc_roles_types(database_connector, npc_roles_types)

    # -------------------------------------- OBJECTS -----------------------------------------

    object_types = load_json(PATH_OBJECT_TYPES_JSON)
    seed_object_types(database_connector, object_types)

    items = load_json(PATH_DIR_ITEMS)
    seed_items(database_connector, items)

    database_connector.disconnect()


if __name__ == '__main__':
    main()
    print('Game database seeded successfully')
