import os

from database.accounts_database_init import ACCOUNTS_DATABASE_NAME
from database.game_database_init import GAME_DATABASE_NAME

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIR_DATABASE: str = os.path.join(PROJECT_ROOT, 'database')

USERS_DATABASE_PATH: str = os.path.join(DIR_DATABASE, ACCOUNTS_DATABASE_NAME)
GAME_DATABASE_PATH: str = os.path.join(DIR_DATABASE, GAME_DATABASE_NAME)

DIR_DATA: str = 'data'
DIR_DATABASE_DATA: str = os.path.join(DIR_DATABASE, DIR_DATA)

PATH_DIR_ITEMS: str = os.path.join(DIR_DATABASE_DATA, 'items')
PATH_KILL_SERIES_TITLES_JSON: str = os.path.join(DIR_DATABASE_DATA, 'kill_series_titles.json')
PATH_CURRENCIES_JSON: str = os.path.join(DIR_DATABASE_DATA, 'currencies.json')
PATH_RARITIES_JSON: str = os.path.join(DIR_DATABASE_DATA, 'rarities.json')
PATH_FACTIONS_JSON: str = os.path.join(DIR_DATABASE_DATA, 'factions.json')
PATH_EQUIPMENT_SLOTS_JSON: str = os.path.join(DIR_DATABASE_DATA, 'equipment_slots.json')
PATH_ITEM_CATEGORIES_JSON: str = os.path.join(DIR_DATABASE_DATA, 'item_categories.json')
PATH_ATTRIBUTES_JSON: str = os.path.join(DIR_DATABASE_DATA, 'attributes.json')
PATH_NPC_ROLES_TYPES_JSON: str = os.path.join(DIR_DATABASE_DATA, 'npc_roles_types.json')
PATH_MAPS_JSON: str = os.path.join(DIR_DATABASE_DATA, 'maps.json')
PATH_NPCS_JSON: str = os.path.join(DIR_DATABASE_DATA, 'npcs.json')
DIR_DATABASE_OBJECTS: str = os.path.join(DIR_DATABASE_DATA, 'objects')
PATH_OBJECT_TYPES_JSON: str = os.path.join(DIR_DATABASE_OBJECTS, 'object_types.json')
PATH_OBJECTS_JSON: str = os.path.join(DIR_DATABASE_DATA, 'objects.json')
PATH_MAP_NPC_POSITIONS_JSON: str = os.path.join(DIR_DATABASE_DATA, 'map_npc_positions.json')

DIR_ASSETS: str = os.path.join(PROJECT_ROOT, 'assets')

DIR_PROJECT: str = 'project'
PATH_ASSETS_PROJECT: str = os.path.join(DIR_ASSETS, DIR_PROJECT)
PATH_IMAGE_START_SCREEN: str = os.path.join(PATH_ASSETS_PROJECT, 'start_screen.png')
PATH_IMAGE_NAME: str = os.path.join(PATH_ASSETS_PROJECT, 'name.png')
PATH_IMAGE_LOGO: str = os.path.join(PATH_ASSETS_PROJECT, 'logo.png')

DIR_NPC_MARKERS: str = 'entity_markers'
DIR_ASSETS_NPC_MARKERS: str = os.path.join(DIR_ASSETS, DIR_NPC_MARKERS)

DIR_PORTRAITS: str = 'portraits'
DIR_ASSETS_PORTRAITS: str = os.path.join(DIR_ASSETS, DIR_PORTRAITS)

DIR_CURSORS: str = 'cursors'
DIR_ASSETS_CURSORS: str = os.path.join(DIR_ASSETS, DIR_CURSORS)

DIR_FONTS: str = 'fonts'
DIR_ASSETS_FONTS: str = os.path.join(DIR_ASSETS, DIR_FONTS)
PATH_FONT_ALICE_IN_WONDERLAND: str = os.path.join(DIR_ASSETS_FONTS, 'AliceInWonderland.ttf')

DIR_ITEM_ICONS: str = 'item_icons'
DIR_ASSETS_ITEM_ICONS: str = os.path.join(DIR_ASSETS, DIR_ITEM_ICONS)

DIR_SPELL_ICONS: str = 'spell_icons'
DIR_ASSETS_SPELL_ICONS: str = os.path.join(DIR_ASSETS, DIR_SPELL_ICONS)

DIR_INTERFACE: str = 'interface'
DIR_ASSETS_INTERFACE: str = os.path.join(DIR_ASSETS, DIR_INTERFACE)

DIR_LOOT: str = os.path.join(DIR_ASSETS, 'loot')
PATH_ICON_LOOT: str = os.path.join(DIR_LOOT, 'loot.png')
DIR_ASSETS_LOOT_GOLD: str = os.path.join(DIR_LOOT, 'gold')

PATH_IMAGE_EMPTY_ITEM_SLOT: str = os.path.join(DIR_ASSETS_INTERFACE, 'empty_item_slot.png')
PATH_IMAGE_EMPTY_SPELL_SLOT: str = os.path.join(DIR_ASSETS_INTERFACE, 'empty_spell_slot.png')
PATH_IMAGE_INVENTORY: str = os.path.join(DIR_ASSETS_INTERFACE, 'inventory.png')
PATH_IMAGE_EQUIPMENT: str = os.path.join(DIR_ASSETS_INTERFACE, 'equipment.png')
PATH_IMAGE_HP_POTION: str = os.path.join(DIR_ASSETS_INTERFACE, 'hp_potion.png')
PATH_IMAGE_MANA_POTION: str = os.path.join(DIR_ASSETS_INTERFACE, 'mana_potion.png')
PATH_IMAGE_TOWN_PORTAL: str = os.path.join(DIR_ASSETS_INTERFACE, 'town_portal.png')
PATH_IMAGE_MOON: str = os.path.join(DIR_ASSETS_INTERFACE, 'moon.png')
PATH_IMAGE_SUN: str = os.path.join(DIR_ASSETS_INTERFACE, 'sun.png')

DIR_CURRENCIES: str = 'currencies'
DIR_ASSETS_CURRENCIES: str = os.path.join(DIR_ASSETS, DIR_CURRENCIES)

DIR_MAP_LOADING_SCREENS: str = 'map_loading_screens'
DIR_ASSETS_MAP_LOADING_SCREENS: str = os.path.join(DIR_ASSETS, DIR_MAP_LOADING_SCREENS)

DIR_SOUNDS: str = 'sounds'
DIR_ASSETS_SOUNDS: str = os.path.join(DIR_ASSETS, DIR_SOUNDS)
DIR_ASSETS_SOUNDS_NPC: str = os.path.join(DIR_ASSETS, DIR_SOUNDS, 'npc')

DIR_SOUNDTRACKS: str = 'soundtracks'
DIR_ASSETS_SOUNDTRACKS: str = os.path.join(DIR_ASSETS, DIR_SOUNDTRACKS)

FILE_LOGIN_SCREEN_SOUNDTRACK: str = 'forest_hut.mp3'
PATH_LOGIN_SCREEN_SOUNDTRACK: str = os.path.join(DIR_ASSETS_SOUNDTRACKS, FILE_LOGIN_SCREEN_SOUNDTRACK)

FILE_SOUNDTRACK_DAY: str = 'day.mp3'
FILE_SOUNDTRACK_NIGHT: str = 'night.mp3'

DIR_SPRITES: str = 'sprites'
DIR_ASSETS_SPRITES: str = os.path.join(DIR_ASSETS, DIR_SPRITES)
DIR_ASSETS_SPRITES_CHARACTERS: str = os.path.join(DIR_ASSETS_SPRITES, 'characters')
DIR_ASSETS_SPRITES_OBJECTS: str = os.path.join(DIR_ASSETS_SPRITES, 'interactive_objects')

DIR_QUOTES: str = os.path.join(DIR_DATABASE, 'quotes')
PATH_JSON_ENEMY_COMMON_QUOTES: str = os.path.join(DIR_QUOTES, 'enemy_common_quotes.json')
PATH_JSON_NPC_COMMON_QUOTES: str = os.path.join(DIR_QUOTES, 'npc_common_quotes.json')
PATH_JSON_PLAYER_COMMON_QUOTES: str = os.path.join(DIR_QUOTES, 'player_common_quotes.json')
PATH_JSON_RETURN_TO_TOWN_QUOTES: str = os.path.join(DIR_QUOTES, 'return_to_town_quotes.json')

PATH_JSON_CENSORED_WORDS: str = os.path.join(DIR_DATABASE, 'censored_words.json')

DIR_MAPS: str = 'maps'
DIR_DATABASE_MAPS: str = os.path.join(DIR_DATABASE, DIR_MAPS)
TXT_COLLISIONS_GRID: str = 'collision_grid.txt'

DIR_WHATSNEW: str = os.path.join(PROJECT_ROOT, 'patch_notes')
