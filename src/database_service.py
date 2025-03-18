import sqlite3

from database.game_database_table_columns_names import MapObjectPositionsTable, MapsTable, ObjectsTable, \
    MapNpcPositionsTable, NpcsTable, NpcRolesTable, NpcRolesTypesTable, CharactersTable, CharacterAttributesTable, \
    AttributesTable, ItemsTable, CharacterEquipmentTable, CurrenciesTable, CharacterCurrenciesTable, \
    CharacterBankLimitsTable, CharacterInventoryLimitsTable, CharacterInventoryTable, EquipmentSlotsTable, \
    NpcAttributesTable, KillSeriesTitlesTable, ObjectTypesTable, CharacterSpellsTable, SpellsTable, NpcSpellsTable, \
    CharacterPositionsTable, FactionsTable, MapFadingWallPositionsTable, MapFadingWallsTable
from src.paths import GAME_DATABASE_PATH


class DatabaseService:

    @staticmethod
    def _connect():
        conn = sqlite3.connect(GAME_DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def get_kill_series_titles():
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {KillSeriesTitlesTable.TITLE_NAME}, {KillSeriesTitlesTable.MIN_KILLS}
                FROM {KillSeriesTitlesTable._TABLE_NAME}
                ORDER BY {KillSeriesTitlesTable.TITLE_ID}
                '''
            )

            return [{title_name: min_kills} for title_name, min_kills in cursor.fetchall()]

    @staticmethod
    def get_map_info(map_id) -> dict | None:
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {MapsTable._TABLE_NAME}
                WHERE {MapsTable.MAP_ID} = ?
                ''',
                (
                    map_id,
                )
            )
            map_data = cursor.fetchone()
            return dict(map_data)

    @staticmethod
    def get_objects_on_map(map_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {MapObjectPositionsTable.OBJECT_ID}, {MapObjectPositionsTable.X}, {MapObjectPositionsTable.Y}
                FROM {MapObjectPositionsTable._TABLE_NAME}
                WHERE {MapObjectPositionsTable.MAP_ID} = ?
                ''',
                (
                    map_id,
                )
            )

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_objects_by_ids(object_ids):
        if not object_ids:
            return []

        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {ObjectsTable._TABLE_NAME}
                WHERE {ObjectsTable.OBJECT_ID} IN ({','.join(['?'] * len(object_ids))})
                ''',
                tuple(object_ids))

            return {row[ObjectsTable.OBJECT_ID]: dict(row) for row in cursor.fetchall()}

    @staticmethod
    def get_object_types():
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {ObjectTypesTable._TABLE_NAME}
                '''
            )

            return {row[ObjectTypesTable.OBJECT_TYPE_ID]: dict(row) for row in cursor.fetchall()}

    @staticmethod
    def get_object_type_data(table_name, object_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {table_name}
                WHERE {ObjectsTable.OBJECT_ID} = ?
                ''',
                (
                    object_id,
                )
            )

            return cursor.fetchone()

    @staticmethod
    def get_map_npc_positions(map_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {MapNpcPositionsTable.NPC_ID}, {MapNpcPositionsTable.X}, {MapNpcPositionsTable.Y}
                FROM {MapNpcPositionsTable._TABLE_NAME}
                WHERE {MapNpcPositionsTable.MAP_ID} = ?
                ''',
                (
                    map_id,
                )
            )

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_npcs_by_ids(npc_ids):
        if not npc_ids:
            return []

        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {NpcsTable._TABLE_NAME}
                WHERE {NpcsTable.NPC_ID} IN ({','.join(['?'] * len(npc_ids))})
                ''',
                tuple(npc_ids))

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_npc_roles_names(npc_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {NpcRolesTypesTable.NPC_ROLE_NAME}
                FROM {NpcRolesTable._TABLE_NAME}
                JOIN {NpcRolesTypesTable._TABLE_NAME}
                ON {NpcRolesTable.NPC_ROLE_TYPE_ID} = {NpcRolesTypesTable.NPC_ROLE_TYPE_ID}
                WHERE {NpcRolesTable.NPC_ID} = ?
                ''',
                (
                    npc_id,
                )
            )
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def get_character_data(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT * 
                FROM {CharactersTable._TABLE_NAME}
                WHERE {CharactersTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )

            character_data = cursor.fetchone()

            if character_data is None:
                return None

            return dict(character_data)

    @staticmethod
    def get_character_position(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {CharacterPositionsTable._TABLE_NAME}
                WHERE {CharacterPositionsTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )

            return dict(cursor.fetchone())

    @staticmethod
    def get_faction_name(faction_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {FactionsTable.FACTION_NAME}
                FROM {FactionsTable._TABLE_NAME}
                WHERE {FactionsTable.FACTION_ID} = ?
                ''',
                (
                    faction_id,
                )
            )

            return cursor.fetchone()

    @staticmethod
    def get_character_spells(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT s.*
                FROM {CharacterSpellsTable._TABLE_NAME} cs
                JOIN {SpellsTable._TABLE_NAME} s ON cs.{CharacterSpellsTable.SPELL_ID} = s.{SpellsTable.SPELL_ID}
                WHERE cs.{CharacterSpellsTable.CHARACTER_ID} = ?
                ''',
                (character_id,)
            )

            return cursor.fetchall()

    @staticmethod
    def get_npc_spells(npc_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT s.*
                FROM {NpcSpellsTable._TABLE_NAME} ns
                JOIN {SpellsTable._TABLE_NAME} s ON ns.{NpcSpellsTable.SPELL_ID} = s.{SpellsTable.SPELL_ID}
                WHERE cs.{NpcSpellsTable.NPC_ID} = ?
                ''',
                (npc_id,)
            )

            return cursor.fetchall()

    @staticmethod
    def get_character_attributes(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT a.{AttributesTable.ATTRIBUTE_NAME}, ca.{CharacterAttributesTable.ATTRIBUTE_VALUE}
                FROM {CharacterAttributesTable._TABLE_NAME} ca
                JOIN {AttributesTable._TABLE_NAME} a ON ca.{CharacterAttributesTable.ATTRIBUTE_ID} = a.{AttributesTable.ATTRIBUTE_ID}
                WHERE ca.{CharacterAttributesTable.CHARACTER_ID} = ?
                ''',
                (character_id,)
            )

            return {attribute_name: value for attribute_name, value in cursor.fetchall()}

    @staticmethod
    def get_npc_attributes(npc_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT a.{AttributesTable.ATTRIBUTE_NAME}, na.{NpcAttributesTable.ATTRIBUTE_VALUE}
                FROM {NpcAttributesTable._TABLE_NAME} na
                JOIN {AttributesTable._TABLE_NAME} a ON na.{NpcAttributesTable.ATTRIBUTE_ID} = a.{AttributesTable.ATTRIBUTE_ID}
                WHERE na.{NpcAttributesTable.NPC_ID} = ?
                ''',
                (npc_id,)
            )

            return {attribute_name: value for attribute_name, value in cursor.fetchall()}

    @staticmethod
    def get_item(item_id) -> dict | None:
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {ItemsTable._TABLE_NAME}
                WHERE {ItemsTable.ITEM_ID} = ?
                ''',
                (item_id,)
            )
            item_data = cursor.fetchone()

            return dict(item_data)

    @staticmethod
    def get_items(item_ids):
        if not item_ids:
            return []

        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {ItemsTable._TABLE_NAME}
                WHERE {ItemsTable.ITEM_ID} IN ({','.join(['?'] * len(item_ids))})
                ''',
                tuple(item_ids, )
            )

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_random_items(how_many, allow_recursive=True):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {ItemsTable._TABLE_NAME}
                ORDER BY RANDOM()
                LIMIT (?)
                ''',
                (
                    how_many,
                )
            )
            items = [dict(row) for row in cursor.fetchall()]
            if allow_recursive:
                while len(items) < how_many:
                    items.extend(DatabaseService.get_random_items(how_many - len(items), allow_recursive=False))

            return items

    @staticmethod
    def get_equipment_slots():
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {EquipmentSlotsTable._TABLE_NAME}
                '''
            )

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_equipment_slot_id(equipment_slot_name):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {EquipmentSlotsTable._TABLE_NAME}
                WHERE {EquipmentSlotsTable.EQUIPMENT_SLOT_NAME} = ?
                ''',
                (
                    equipment_slot_name,
                )
            )

            return cursor.fetchone()

    @staticmethod
    def get_character_equipped_items(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {CharacterEquipmentTable.EQUIPMENT_SLOT_ID}, {CharacterEquipmentTable.ITEM_ID}
                FROM {CharacterEquipmentTable._TABLE_NAME}
                WHERE {CharacterEquipmentTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_character_currencies(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT c.{CurrenciesTable.CURRENCY_NAME}, cc.{CharacterCurrenciesTable.AMOUNT} 
                FROM {CharacterCurrenciesTable._TABLE_NAME} cc
                JOIN {CurrenciesTable._TABLE_NAME} c ON cc.{CharacterCurrenciesTable.CURRENCY_ID} = c.{CurrenciesTable.CURRENCY_ID}
                WHERE cc.{CharacterCurrenciesTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )

            currencies_data = cursor.fetchall()

            return {currency_name: amount for currency_name, amount in currencies_data}

    @staticmethod
    def get_character_inventory(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {CharacterInventoryTable._TABLE_NAME}
                WHERE {CharacterInventoryTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_character_inventory_limits(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {CharacterInventoryLimitsTable.MAX_SLOTS}
                FROM {CharacterInventoryLimitsTable._TABLE_NAME}
                WHERE {CharacterInventoryLimitsTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )
            inventory_limits_data = cursor.fetchone()
            return inventory_limits_data[0]

    @staticmethod
    def get_character_bank_limits(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {CharacterBankLimitsTable.MAX_SLOTS}
                FROM {CharacterBankLimitsTable._TABLE_NAME}
                WHERE {CharacterBankLimitsTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )
            bank_limits_data = cursor.fetchone()
            return bank_limits_data

    @staticmethod
    def get_character_free_inventory_slot_nr(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {CharacterInventoryTable.SLOT_NR}
                FROM {CharacterInventoryTable._TABLE_NAME}
                WHERE {CharacterInventoryTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )

            used_slots = {row[0] for row in cursor.fetchall()}

            free_slot = 1
            while free_slot in used_slots:
                free_slot += 1

            return free_slot

    @staticmethod
    def add_item_to_character_inventory(character_id, item_id, item_quantity):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            slot_nr = DatabaseService.get_character_free_inventory_slot_nr(character_id)
            character_inventory_limits = DatabaseService.get_character_inventory_limits(character_id)

            if slot_nr > character_inventory_limits[0]:
                return

            cursor.execute(
                f'''
                INSERT INTO {CharacterInventoryTable._TABLE_NAME} (
                    {CharacterInventoryTable.CHARACTER_ID},
                    {CharacterInventoryTable.ITEM_ID},
                    {CharacterInventoryTable.ITEM_QUANTITY},
                    {CharacterInventoryTable.SLOT_NR}
                ) VALUES (?, ?, ?, ?)
                ''',
                (
                    character_id,
                    item_id,
                    item_quantity,
                    slot_nr
                )
            )

    @staticmethod
    def get_character_equipped_item_id(character_id, equipment_slot_name):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            equipment_slot_id = DatabaseService.get_equipment_slot_id(equipment_slot_name)

            cursor.execute(
                f'''
                SELECT {CharacterEquipmentTable.ITEM_ID}
                FROM {CharacterEquipmentTable._TABLE_NAME}
                WHERE {CharacterEquipmentTable.CHARACTER_ID} = ? AND {CharacterEquipmentTable.EQUIPMENT_SLOT_ID} = ?
                ''',
                (
                    character_id,
                    equipment_slot_id
                )
            )

            return cursor.fetchone()

    @staticmethod
    def add_item_to_character_equipment(character_id, item_id, equipment_slot_name):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            equipment_slot_id = DatabaseService.get_equipment_slot_id(equipment_slot_name)

            cursor.execute(
                f'''
                UPDATE {CharacterEquipmentTable._TABLE_NAME}
                SET {CharacterEquipmentTable.ITEM_ID} = ?
                WHERE {CharacterEquipmentTable.CHARACTER_ID} = ? AND {CharacterEquipmentTable.EQUIPMENT_SLOT_ID} = ?
                ''',
                (
                    item_id,
                    character_id,
                    equipment_slot_id
                )
            )

    @staticmethod
    def delete_character(character_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                DELETE FROM {CharactersTable._TABLE_NAME}
                WHERE {CharactersTable.CHARACTER_ID} = ?
                ''',
                (
                    character_id,
                )
            )

    @staticmethod
    def get_map_fading_wall_positions(map_id):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT *
                FROM {MapFadingWallPositionsTable._TABLE_NAME}
                WHERE {MapFadingWallPositionsTable.MAP_ID} = ?
                ''',
                (
                    map_id,
                )
            )

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_map_fading_walls(fading_wall_ids):
        with DatabaseService._connect() as conn:
            cursor = conn.cursor()

            cursor.executemany(
                f'''
                SELECT *
                FROM {MapFadingWallsTable._TABLE_NAME}
                WHERE {MapFadingWallsTable.FADING_WALL_ID} = ?
                ''',
                fading_wall_ids
            )

            return {row[MapFadingWallsTable.FADING_WALL_ID]: dict(row) for row in cursor.fetchall()}
