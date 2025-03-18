import sqlite3

import bcrypt

from database.accounts_database_table_columns_names import AccountsTable
from src.paths import USERS_DATABASE_PATH


class AccountsManager:
    _instance = None
    _account_name = None
    _account_id = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    @classmethod
    def is_user_logged_in(cls):
        return cls._account_name is not None

    @classmethod
    def get_account_name(cls):
        return cls._account_name

    @classmethod
    def get_account_id(cls):
        return cls._account_id

    @staticmethod
    def is_password_valid(provided_password: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

    @classmethod
    def authorize(cls, account_name: str, provided_password: str) -> bool:
        try:
            conn = sqlite3.connect(USERS_DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute(
                f'''
                SELECT {AccountsTable.ACCOUNT_ID}, {AccountsTable.PASSWORD_HASH}
                FROM accounts
                WHERE {AccountsTable.ACCOUNT_NAME} = ?
                ''',
                (account_name,))
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                stored_password_hash = result[1]
                if cls.is_password_valid(provided_password, stored_password_hash):
                    cls._account_name = account_name
                    cls._account_id = user_id
                    return True

            return False

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
