from enum import Enum

from src.colors import RED, ORANGE, GREEN, LIGHT_GREEN, YELLOW, WHITE


class ChatMessageColorType(Enum):
    NORMAL = WHITE
    SYSTEM = YELLOW
    PLAYER = LIGHT_GREEN
    ENEMY = RED
    NPC = GREEN
    ERROR = RED
    LEGENDARY_DROP = ORANGE
    PLAYER_DEATH = RED
