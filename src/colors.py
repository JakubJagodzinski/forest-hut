from src.enums.rarity_type import RarityType

WHITE = (255, 255, 255)
GRAY = (26, 28, 26)
LIGHT_GRAY = (89, 92, 89)
BLACK = (0, 0, 0)
RED = (105, 14, 7)
LIGHT_RED = (247, 35, 35)
BLUE = (6, 14, 71)
LIGHT_BLUE = (100, 100, 200)
SEA_BLUE = (100, 200, 200)
GREEN = (9, 77, 6)
GRAY_GREEN = (91, 92, 80)
LIGHT_GREEN = (100, 200, 100)
YELLOW = (200, 200, 100)
ORANGE = (200, 100, 100)
PURPLE = (94, 25, 79)

RARITY_COLORS = {
    RarityType.POOR: LIGHT_GRAY,
    RarityType.COMMON: YELLOW,
    RarityType.UNCOMMON: LIGHT_GREEN,
    RarityType.RARE: LIGHT_BLUE,
    RarityType.EPIC: PURPLE,
    RarityType.LEGENDARY: ORANGE,
    RarityType.MYTHIC: SEA_BLUE
}
