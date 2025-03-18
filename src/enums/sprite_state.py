from enum import StrEnum


class SpriteState(StrEnum):
    IDLE = 'idle'
    RUN = 'run'
    HURT = 'hurt'
    DEAD = 'dead'
    BASE_ATTACK = 'attack1'
    SPECIAL_ATTACK = 'attack2'
    DEATH = 'death'
    INTERACT = 'interact'
    FINAL = 'final'
