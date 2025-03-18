from enum import StrEnum


class CharacterAttributeType(StrEnum):
    MAX_HP = 'max_hp'
    HP = 'hp'
    HP_REGENERATION_RATE = 'hp_regeneration_rate'
    MAX_MANA = 'max_mana'
    MANA = 'mana'
    MANA_REGENERATION_RATE = 'mana_regeneration_rate'
    MAX_STAMINA = 'max_stamina'
    STAMINA = 'stamina'
    STAMINA_REGENERATION_RATE = 'stamina_regeneration_rate'
    ATTACK_SPEED = 'attack_speed'
    DAMAGE = 'damage'
    ATTACK_DISTANCE = 'attack_distance'
    MOVEMENT_SPEED = 'movement_speed'
    ACTIVATION_DISTANCE = 'activation_distance'
