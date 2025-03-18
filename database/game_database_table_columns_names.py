from enum import StrEnum


class RaritiesTable(StrEnum):
    _TABLE_NAME = 'rarities'
    RARITY_ID = 'rarity_id'
    RARITY_NAME = 'rarity_name'


class FactionsTable(StrEnum):
    _TABLE_NAME = 'factions'
    FACTION_ID = 'faction_id'
    FACTION_NAME = 'faction_name'


class AttributesTable(StrEnum):
    _TABLE_NAME = 'attributes'
    ATTRIBUTE_ID = 'attribute_id'
    ATTRIBUTE_NAME = 'attribute_name'


class SpellsTable(StrEnum):
    _TABLE_NAME = 'spells'
    SPELL_ID = 'spell_id'
    SPELL_NAME = 'spell_name'
    CAST_TIME = 'cast_time'
    COOLDOWN_TIME = 'cooldown_time'


class CharacterSpellsTable(StrEnum):
    _TABLE_NAME = 'character_spells'
    CHARACTER_ID = 'character_id'
    SPELL_ID = 'spell_id'


class NpcSpellsTable(StrEnum):
    _TABLE_NAME = 'npc_spells'
    NPC_ID = 'npc_id'
    SPELL_ID = 'spell_id'


class EquipmentSlotsTable(StrEnum):
    _TABLE_NAME = 'equipment_slots'
    EQUIPMENT_SLOT_ID = 'equipment_slot_id'
    EQUIPMENT_SLOT_NAME = 'equipment_slot_name'


class CurrenciesTable(StrEnum):
    _TABLE_NAME = 'currencies'
    CURRENCY_ID = 'currency_id'
    CURRENCY_NAME = 'currency_name'
    MAX_AMOUNT = 'max_amount'


class ItemCategoriesTable(StrEnum):
    _TABLE_NAME = 'item_categories'
    CATEGORY_ID = 'category_id'
    PARENT_CATEGORY_ID = 'parent_category_id'
    CATEGORY_NAME = 'category_name'
    CATEGORY_DESCRIPTION = 'category_description'


class ItemsTable(StrEnum):
    _TABLE_NAME = 'items'
    ITEM_ID = 'item_id'
    CATEGORY_ID = 'category_id'
    EQUIPMENT_SLOT_ID = 'equipment_slot_id'
    ICON_NAME = 'icon_name'
    ITEM_NAME = 'item_name'
    ITEM_DESCRIPTION = 'item_description'
    RARITY_ID = 'rarity_id'
    REQUIRED_LVL = 'required_lvl'
    STACK_SIZE = 'stack_size'
    ITEM_VALUE = 'item_value'


class ItemAttributesTable(StrEnum):
    _TABLE_NAME = 'item_attributes'
    ATTRIBUTE_ID = 'attribute_id'
    ITEM_ID = 'item_id'
    ATTRIBUTE_VALUE = 'attribute_value'


class KillSeriesTitlesTable(StrEnum):
    _TABLE_NAME = 'kill_series_titles'
    TITLE_ID = 'title_id'
    TITLE_NAME = 'title_name'
    MIN_KILLS = 'min_kills'


class MapsTable(StrEnum):
    _TABLE_NAME = 'maps'
    MAP_ID = 'map_id'
    MAP_NAME = 'map_name'
    MIN_LVL = 'min_lvl'
    MAX_LVL = 'max_lvl'


class NpcAttributesTable(StrEnum):
    _TABLE_NAME = 'npc_attributes'
    NPC_ID = 'npc_id'
    ATTRIBUTE_ID = 'attribute_id'
    ATTRIBUTE_VALUE = 'attribute_value'


class NpcsTable(StrEnum):
    _TABLE_NAME = 'npcs'
    NPC_ID = 'npc_id'
    NPC_NAME = 'npc_name'
    SPRITE_NAME = 'sprite_name'
    RARITY_ID = 'rarity_id'
    FACTION_ID = 'faction_id'
    STATUS_ID = 'status_id'
    LVL = 'lvl'


class NpcRolesTypesTable(StrEnum):
    _TABLE_NAME = 'npc_roles_types'
    NPC_ROLE_TYPE_ID = 'npc_role_type_id'
    NPC_ROLE_NAME = 'npc_role_name'
    NPC_ROLE_TABLE_NAME = 'npc_role_table_name'


class NpcRolesTable(StrEnum):
    _TABLE_NAME = 'npc_roles'
    NPC_ID = 'npc_id'
    NPC_ROLE_TYPE_ID = 'npc_role_type_id'


class MapNpcPositionsTable(StrEnum):
    _TABLE_NAME = 'map_npc_positions'
    MAP_NPC_ID = 'map_npc_id'
    MAP_ID = 'map_id'
    NPC_ID = 'npc_id'
    X = 'x'
    Y = 'y'


class VendorItemsTable(StrEnum):
    _TABLE_NAME = 'vendor_items'
    VENDOR_ID = 'vendor_id'
    ITEM_ID = 'item_id'


class ObjectTypesTable(StrEnum):
    _TABLE_NAME = 'object_types'
    OBJECT_TYPE_ID = 'object_type_id'
    OBJECT_TYPE_NAME = 'object_type_name'
    OBJECT_TYPE_TABLE_NAME = 'object_type_table_name'


class ObjectsTable(StrEnum):
    _TABLE_NAME = 'objects'
    OBJECT_ID = 'object_id'
    OBJECT_TYPE_ID = 'object_type_id'
    OBJECT_NAME = 'object_name'
    SPRITE_NAME = 'sprite_name'


class LootableObjectItems(StrEnum):
    _TABLE_NAME = 'lootable_object_items'
    OBJECT_ID = 'object_id'
    ITEM_ID = 'item_id'


class LocationChangersTable(StrEnum):
    _TABLE_NAME = 'location_changers'
    OBJECT_ID = 'object_id'
    DESTINATION_MAP_ID = 'destination_map_id'
    DESTINATION_X = 'destination_x'
    DESTINATION_Y = 'destination_y'


class MapObjectPositionsTable(StrEnum):
    _TABLE_NAME = 'map_object_positions'
    MAP_OBJECT_ID = 'map_object_id'
    MAP_ID = 'map_id'
    OBJECT_ID = 'object_id'
    X = 'x'
    Y = 'y'


class CharactersTable(StrEnum):
    _TABLE_NAME = 'characters'
    CHARACTER_ID = 'character_id'
    ACCOUNT_ID = 'account_id'
    IS_HARDCORE = 'is_hardcore'
    CHARACTER_NAME = 'character_name'
    FACTION_ID = 'faction_id'
    LVL = 'lvl'
    XP = 'xp'


class CharacterPositionsTable(StrEnum):
    _TABLE_NAME = 'character_positions'
    CHARACTER_ID = 'character_id'
    MAP_ID = 'map_id'
    X = 'x'
    Y = 'y'


class CharacterAttributesTable(StrEnum):
    _TABLE_NAME = 'character_attributes'
    ATTRIBUTE_ID = 'attribute_id'
    CHARACTER_ID = 'character_id'
    ATTRIBUTE_VALUE = 'attribute_value'


class CharacterBankLimitsTable(StrEnum):
    _TABLE_NAME = 'character_bank_limits'
    CHARACTER_ID = 'character_id'
    MAX_SLOTS = 'max_slots'


class CharacterBankTable(StrEnum):
    _TABLE_NAME = 'character_bank'
    CHARACTER_ID = 'character_id'
    ITEM_ID = 'item_id'
    SLOT_NR = 'slot_nr'


class CharacterCurrenciesTable(StrEnum):
    _TABLE_NAME = 'character_currencies'
    CHARACTER_ID = 'character_id'
    CURRENCY_ID = 'currency_id'
    AMOUNT = 'amount'


class CharacterEquipmentTable(StrEnum):
    _TABLE_NAME = 'character_equipment'
    CHARACTER_ID = 'character_id'
    EQUIPMENT_SLOT_ID = 'equipment_slot_id'
    ITEM_ID = 'item_id'


class CharacterInventoryLimitsTable(StrEnum):
    _TABLE_NAME = 'character_inventory_limits'
    CHARACTER_ID = 'character_id'
    MAX_SLOTS = 'max_slots'


class CharacterInventoryTable(StrEnum):
    _TABLE_NAME = 'character_inventory'
    CHARACTER_ID = 'character_id'
    ITEM_ID = 'item_id'
    ITEM_QUANTITY = 'item_quantity'
    SLOT_NR = 'slot_nr'


class MapFadingWallsTable(StrEnum):
    _TABLE_NAME = 'map_fading_walls'
    FADING_WALL_ID = 'fading_wall_id'
    IMAGE_PATH = 'image_path'
    WALL_WIDTH = 'wall_width'
    WALL_HEIGHT = 'wall_height'


class MapFadingWallPositionsTable(StrEnum):
    _TABLE_NAME = 'map_fading_wall_positions'
    MAP_FADING_WALL_POSITION_ID = 'map_fading_wall_position_id'
    FADING_WALL_ID = 'fading_wall_id'
    MAP_ID = 'map_id'
    X = 'x'
    Y = 'y'
