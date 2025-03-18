from enum import StrEnum


class AccountsTable(StrEnum):
    _TABLE_NAME = 'accounts'
    ACCOUNT_ID = 'account_id'
    ACCOUNT_NAME = 'account_name'
    PASSWORD_HASH = 'password_hash'
    CREATED_AT = 'created_at'
