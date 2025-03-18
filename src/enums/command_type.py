from enum import StrEnum


class CommandType(StrEnum):
    QUIT = 'quit'
    GAME_TIME = 'game time'
    POSITION = 'position'
