import sqlite3

from database.accounts_database_table_columns_names import AccountsTable
from database.database_config import ACCOUNTS_DATABASE_NAME

ACCOUNT_NAME_MIN_LENGTH = 3
ACCOUNT_NAME_MAX_LENGTH = 20


def create_accounts_database():
    database_connection = sqlite3.connect(ACCOUNTS_DATABASE_NAME)
    cursor = database_connection.cursor()

    cursor.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {AccountsTable._TABLE_NAME} (
            {AccountsTable.ACCOUNT_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {AccountsTable.ACCOUNT_NAME} TEXT UNIQUE NOT NULL CHECK (LENGTH({AccountsTable.ACCOUNT_NAME}) BETWEEN {ACCOUNT_NAME_MIN_LENGTH} AND {ACCOUNT_NAME_MAX_LENGTH}),
            {AccountsTable.PASSWORD_HASH} TEXT NOT NULL,
            {AccountsTable.CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )

    database_connection.commit()
    database_connection.close()


if __name__ == '__main__':
    create_accounts_database()
    print('Accounts database created successfully')
