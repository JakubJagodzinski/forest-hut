from enum import StrEnum


class ErrorMessageType(StrEnum):
    INVENTORY_IS_FULL = 'Inventory is full'
    BANK_IS_FULL = 'Bank is full'
    NOT_READY_YET = 'It\'s not ready yet'
    NOT_ENOUGH_MANA = 'Not enough mana'
    NOT_ENOUGH_CURRENCY = 'Not enough currency'
    YOUR_LVL_IS_TOO_LOW = 'Your level is too low'
    YOU_CANT_DO_THAT = 'You can\'t do that'
    YOU_ARE_IN_COMBAT = 'You are in combat!'
    YOU_ARE_DEAD = 'You are dead'
    YOU_ARE_ALREADY_IN_TOWN = 'You are already in a town'
    HEALTH_IS_FULL = 'Health is full'
    MANA_IS_FULL = 'Mana is full'
    CANT_EQUIP_THAT = 'Can\'t equip that'
