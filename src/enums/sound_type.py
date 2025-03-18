from enum import StrEnum


class SoundType(StrEnum):
    HIT = 'hit'
    DEATH = 'death'
    HURT = 'hurt'
    GAME_OVER = 'game_over'
    LEVEL_UP = 'level_up'
    KILL_SERIES_END = 'kill_series_end'
    ARMOR_HIT = 'armor_hit'
