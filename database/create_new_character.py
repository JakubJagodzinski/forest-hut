from database.accounts_database_init import ACCOUNTS_DATABASE_NAME
from database.accounts_database_table_columns_names import AccountsTable
from database.database_connector import DatabaseConnector
from database.game_database_init import GAME_DATABASE_NAME
from database.game_database_table_columns_names import CharactersTable, CharacterInventoryLimitsTable, \
    CharacterBankLimitsTable, CurrenciesTable, CharacterCurrenciesTable, AttributesTable, \
    CharacterAttributesTable, CharacterPositionsTable
from src.enums.character_attribute_type import CharacterAttributeType

CHARACTER_START_MAP_ID = 1
CHARACTER_START_X = 1200
CHARACTER_START_Y = 850

CHARACTER_ATTRIBUTES_START_VALUES = {
    CharacterAttributeType.MAX_HP: 100,
    CharacterAttributeType.HP: 100,
    CharacterAttributeType.HP_REGENERATION_RATE: 5,

    CharacterAttributeType.MAX_MANA: 100,
    CharacterAttributeType.MANA: 100,
    CharacterAttributeType.MANA_REGENERATION_RATE: 5,

    CharacterAttributeType.MAX_STAMINA: 100,
    CharacterAttributeType.STAMINA: 100,
    CharacterAttributeType.STAMINA_REGENERATION_RATE: 5,

    CharacterAttributeType.DAMAGE: 10,
    CharacterAttributeType.ATTACK_DISTANCE: 50,
    CharacterAttributeType.ATTACK_SPEED: 10
}


def get_account_id(account_name):
    database_connector = DatabaseConnector(ACCOUNTS_DATABASE_NAME)
    database_connector.connect()

    database_connector.execute(
        f'''
        SELECT {AccountsTable.ACCOUNT_ID}
        FROM accounts
        WHERE {AccountsTable.ACCOUNT_NAME} = ?
        ''',
        (
            account_name,
        )
    )

    result = database_connector.fetchone()

    database_connector.disconnect()

    if result:
        account_id = result[0]
    else:
        account_id = None

    return account_id


def create_new_character(account_name, character_name):
    database_connector = DatabaseConnector(GAME_DATABASE_NAME)
    database_connector.connect()

    account_id = get_account_id(account_name)

    # ---------------------------------------- CHARACTER ----------------------------------------

    database_connector.execute(
        f'''
        INSERT INTO {CharactersTable._TABLE_NAME} (
            {CharactersTable.ACCOUNT_ID},
            {CharactersTable.CHARACTER_NAME}
        ) VALUES (?, ?)
        ''',
        (
            account_id,
            character_name
        )
    )
    character_id = database_connector.lastrowid

    database_connector.execute(
        f'''
        INSERT INTO {CharacterPositionsTable._TABLE_NAME} (
            {CharacterPositionsTable.CHARACTER_ID},
            {CharacterPositionsTable.MAP_ID},
            {CharacterPositionsTable.X},
            {CharacterPositionsTable.Y})
        VALUES (?, ?, ?, ?)
        ''',
        (
            character_id,
            CHARACTER_START_MAP_ID,
            CHARACTER_START_X,
            CHARACTER_START_Y
        )
    )

    # ---------------------------------------- INVENTORY LIMITS ----------------------------------------

    database_connector.execute(
        f'''
        INSERT INTO {CharacterInventoryLimitsTable._TABLE_NAME} (
            {CharacterInventoryLimitsTable.CHARACTER_ID}
        ) VALUES (?)
        ''',
        (
            character_id,
        )
    )

    # ---------------------------------------- BANK LIMITS ----------------------------------------

    database_connector.execute(
        f'''
        INSERT INTO {CharacterBankLimitsTable._TABLE_NAME} (
            {CharacterBankLimitsTable.CHARACTER_ID}
        ) VALUES (?)
        ''',
        (
            character_id,
        )
    )

    # ---------------------------------------- CURRENCIES ----------------------------------------

    database_connector.execute(
        f'''
        SELECT {CurrenciesTable.CURRENCY_ID}
        FROM {CurrenciesTable._TABLE_NAME}
        '''
    )
    currencies_ids = database_connector.fetchall()

    for currency_id in currencies_ids:
        database_connector.execute(
            f'''
            INSERT INTO {CharacterCurrenciesTable._TABLE_NAME} (
                {CharacterCurrenciesTable.CHARACTER_ID},
                {CharacterCurrenciesTable.CURRENCY_ID}
            ) VALUES (?, ?)
            ''',
            (
                character_id,
                currency_id[0]
            )
        )

    # ---------------------------------------- ATTRIBUTES ----------------------------------------

    for attribute_name, attribute_value in CHARACTER_ATTRIBUTES_START_VALUES.items():
        database_connector.execute(
            f'''
            SELECT {AttributesTable.ATTRIBUTE_ID}
            FROM {AttributesTable._TABLE_NAME}
            WHERE {AttributesTable.ATTRIBUTE_NAME} = (?)
            ''',
            (
                attribute_name,
            )
        )
        attribute_id = database_connector.fetchone()

        database_connector.execute(
            f'''
            INSERT INTO {CharacterAttributesTable._TABLE_NAME} (
                {CharacterAttributesTable.CHARACTER_ID},
                {CharacterAttributesTable.ATTRIBUTE_ID},
                {CharacterAttributesTable.ATTRIBUTE_VALUE}
            ) VALUES (?, ?, ?)
            ''',
            (
                character_id,
                attribute_id[0],
                attribute_value
            )
        )

    database_connector.disconnect()


if __name__ == '__main__':
    create_new_character('jakub', 'player')
