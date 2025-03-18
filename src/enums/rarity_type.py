from enum import StrEnum


class RarityType(StrEnum):
    POOR = 'trash'
    COMMON = 'common'
    UNCOMMON = 'uncommon'
    RARE = 'rare'
    EPIC = 'epic'
    LEGENDARY = 'legendary'
    MYTHIC = 'mythic'
