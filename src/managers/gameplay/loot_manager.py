import os
import random

import pygame

from database.game_database_table_columns_names import ItemsTable
from src.colors import BLACK, WHITE, RARITY_COLORS
from src.common_utils import euclidean_distance
from src.database_service import DatabaseService
from src.entities.character import INTERACTION_DISTANCE
from src.enums.chat_message_color_type import ChatMessageColorType
from src.enums.rarity_type import RarityType
from src.fonts import FONT_MONOSPACE_COURIER_16
from src.interface.interface_constants import BORDER_WIDTH
from src.keybindings import KEY_SWITCH_SHOW_LOOT_NAMES
from src.managers.core.mouse_manager import MouseManager
from src.managers.gameplay.map_manager import MAP_COLLISION_TILE
from src.paths import PATH_ICON_LOOT, DIR_ASSETS_LOOT_GOLD


class LootManager:
    _instance = None

    GENERATE_CHAT_MESSAGE_RARITIES = [
        RarityType.LEGENDARY,
        RarityType.MYTHIC
    ]

    LOOT_PICK_UP_DISTANCE = INTERACTION_DISTANCE
    LOOT_GENERATE_POSITION_DELTA = LOOT_PICK_UP_DISTANCE // 2

    LOOT_NAME_FONT = FONT_MONOSPACE_COURIER_16
    LOOT_NAME_OFFSET_Y = LOOT_PICK_UP_DISTANCE // 2
    LOOT_NAME_PADDING_X = 5

    GOLD_PER_NPC_LEVEL_MIN_VALUE = 10
    GOLD_PER_NPC_LEVEL_MAX_VALUE = 20

    NPC_RARITY_GOLD_BONUS = {
        RarityType.RARE: 0.1,
        RarityType.EPIC: 0.25,
        RarityType.LEGENDARY: 0.5,
        RarityType.MYTHIC: 0.75,
    }

    GOLD_QUANTITY_RANGES = [50, 100, 250, 500, float('inf')]

    LOOT_ICON_SIZE = 50
    GLOW_CENTER = (LOOT_ICON_SIZE // 2, LOOT_ICON_SIZE // 2)

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, screen):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            self.game_surface = screen

            self.player_manager = None
            self.map_manager = None
            self.sound_manager = None
            self.chat_manager = None

            self.current_map_id = None

            self.loot_icon = pygame.image.load(PATH_ICON_LOOT).convert_alpha()
            self.loot_icon = pygame.transform.scale(self.loot_icon, (self.LOOT_ICON_SIZE, self.LOOT_ICON_SIZE))

            self.gold_icons = self.load_gold_icons()

            self.items = {}

            self.gold = {}

            self.draw_loot_names = True

            self.glow_surfaces = {}
            for rarity in RarityType:
                glow_surface = pygame.Surface((self.LOOT_ICON_SIZE, self.LOOT_ICON_SIZE), pygame.SRCALPHA)
                glow_surface.fill((0, 0, 0, 0))
                circle_color = RARITY_COLORS[rarity] + (64,)
                pygame.draw.circle(glow_surface, circle_color, self.GLOW_CENTER, self.LOOT_ICON_SIZE // 2)
                self.glow_surfaces[rarity] = glow_surface

    def setup_references(self):
        from src.managers.gameplay.player_manager import PlayerManager
        from src.managers.ui.chat_manager import ChatManager
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.core.sound_manager import SoundManager

        self.player_manager = PlayerManager.get_instance()
        self.map_manager = MapManager.get_instance()
        self.sound_manager = SoundManager.get_instance()
        self.chat_manager = ChatManager.get_instance()

    def load_gold_icons(self):
        gold_icons = []
        gold_icon_names = os.listdir(DIR_ASSETS_LOOT_GOLD)
        for gold_icon_name in gold_icon_names:
            gold_icon_path = os.path.join(DIR_ASSETS_LOOT_GOLD, gold_icon_name)
            gold_icon = pygame.image.load(gold_icon_path).convert_alpha()
            gold_icon = pygame.transform.scale(gold_icon, (self.LOOT_ICON_SIZE, self.LOOT_ICON_SIZE))
            gold_icons.append(gold_icon)
        return gold_icons

    def update(self):
        self.update_items()
        self.update_gold()

    def update_items(self):
        self.current_map_id = self.map_manager.map_id
        if self.current_map_id not in self.items:
            self.items[self.current_map_id] = []

    def update_gold(self):
        self.current_map_id = self.map_manager.map_id
        if self.current_map_id not in self.gold:
            self.gold[self.current_map_id] = []

    def is_loot_hovered(self, loot_position_on_screen, loot_name):
        loot_screen_x, loot_screen_y = loot_position_on_screen
        if self.draw_loot_names:
            loot_name_text_width, loot_name_text_height = self.LOOT_NAME_FONT.size(loot_name)
            loot_name_x = (loot_screen_x
                           - (loot_name_text_width // 2)
                           - self.LOOT_NAME_PADDING_X)
            loot_name_y = (loot_screen_y
                           - self.LOOT_NAME_OFFSET_Y
                           - loot_name_text_height)
            loot_name_rect = pygame.Rect(
                loot_name_x,
                loot_name_y,
                loot_name_text_width + (2 * self.LOOT_NAME_PADDING_X),
                loot_name_text_height
            )
            return loot_name_rect.collidepoint(pygame.mouse.get_pos())
        else:
            loot_rect = pygame.Rect(
                loot_screen_x - (self.LOOT_ICON_SIZE // 2),
                loot_screen_y - (self.LOOT_ICON_SIZE // 2),
                2 * (self.LOOT_ICON_SIZE // 2),
                2 * (self.LOOT_ICON_SIZE // 2)
            )
            return loot_rect.collidepoint(pygame.mouse.get_pos())

    def is_loot_clicked(self, loot_position_on_screen, loot_name) -> bool:
        return MouseManager.is_left_clicked() and self.is_loot_hovered(loot_position_on_screen, loot_name)

    def is_loot_in_range(self, player_x, player_y, loot_x, loot_y) -> bool:
        return euclidean_distance((player_x, player_y), (loot_x, loot_y)) <= self.LOOT_PICK_UP_DISTANCE

    def pick_item_up(self, player_position) -> tuple[dict, tuple[int, int]] or None:
        player_x, player_y = player_position
        for loot_index, loot in enumerate(self.items[self.current_map_id]):
            item_info, item_quantity, item_position = loot
            item_x, item_y = item_position
            item_position_on_screen = self.map_manager.convert_map_position_to_screen_position(item_x, item_y)
            if self.is_loot_in_range(player_x, player_y, item_x, item_y) and \
                    self.is_loot_clicked(item_position_on_screen, item_info[ItemsTable.ITEM_NAME]):
                del self.items[self.current_map_id][loot_index]
                return (item_info, item_quantity), item_position
        return None

    def pick_gold_up(self, player_position):
        player_x, player_y = player_position
        for gold_index, gold in enumerate(self.gold[self.current_map_id]):
            gold_quantity, gold_position = gold
            gold_x, gold_y = gold_position
            gold_position_on_screen = self.map_manager.convert_map_position_to_screen_position(gold_x, gold_y)
            if self.is_loot_in_range(player_x, player_y, gold_x, gold_y) and \
                    self.is_loot_clicked(gold_position_on_screen, f'{gold_quantity} gold'):
                del self.gold[self.current_map_id][gold_index]
                return gold_quantity, gold_position
        return None

    def drop_loot(self, item_info, item_quantity, drop_position) -> None:
        item_position = (
            drop_position[0] + random.randint(0, MAP_COLLISION_TILE),
            drop_position[1] + random.randint(0, MAP_COLLISION_TILE)
        )
        self.items[self.current_map_id].append((item_info, item_quantity, item_position))

    @staticmethod
    def randomize_drop_position(drop_position) -> tuple[int, int] or None:
        return (
            drop_position[0] + random.randint(0, MAP_COLLISION_TILE // 2),
            drop_position[1] + random.randint(0, MAP_COLLISION_TILE // 2)
        )

    def generate_loot(self, drop_position, min_items=1, max_items=5) -> None:
        number_of_items = random.randint(min_items, max_items)
        items = DatabaseService.get_random_items(number_of_items)
        for item_info in items:
            if item_info[ItemsTable.RARITY_ID] in self.GENERATE_CHAT_MESSAGE_RARITIES:
                self.chat_manager.push_message_to_chat(
                    f'{self.player_manager.name} found [{item_info[ItemsTable.ITEM_NAME]}]!',
                    ChatMessageColorType.LEGENDARY_DROP
                )
            item_position = self.randomize_drop_position(drop_position)
            self.items[self.current_map_id].append([item_info, 1, item_position])

    def generate_gold(self, drop_position, npc_lvl, npc_rarity) -> None:
        gold_quantity = random.randint(
            npc_lvl * self.GOLD_PER_NPC_LEVEL_MIN_VALUE,
            npc_lvl * self.GOLD_PER_NPC_LEVEL_MAX_VALUE
        )
        gold_quantity += gold_quantity * self.NPC_RARITY_GOLD_BONUS.get(npc_rarity, 0)
        gold_position = self.randomize_drop_position(drop_position)
        self.gold[self.current_map_id].append((gold_quantity, gold_position))

    def switch_show_names(self) -> None:
        self.draw_loot_names = not self.draw_loot_names
        state = 'on' if self.draw_loot_names else 'off'
        self.chat_manager.push_message_to_chat(
            f'Loot names are now turned {state} [{chr(KEY_SWITCH_SHOW_LOOT_NAMES)}]',
            ChatMessageColorType.SYSTEM
        )

    def _draw_item_glow(self, item_rarity, item_position_on_screen) -> None:

        item_x, item_y = item_position_on_screen
        self.game_surface.blit(
            self.glow_surfaces[item_rarity],
            (
                item_x - (self.LOOT_ICON_SIZE // 2),
                item_y - (self.LOOT_ICON_SIZE // 2))
        )

    def draw_loot_icon(self, item_position_on_screen) -> None:
        item_x, item_y = item_position_on_screen
        self.game_surface.blit(
            self.loot_icon,
            (
                item_x - (self.LOOT_ICON_SIZE // 2),
                item_y - (self.LOOT_ICON_SIZE // 2)
            )
        )

    def draw_gold_icon(self, gold_position_on_screen, gold_icon) -> None:
        gold_x, gold_y = gold_position_on_screen
        self.game_surface.blit(
            gold_icon,
            (
                gold_x - (self.LOOT_ICON_SIZE // 2),
                gold_y - (self.LOOT_ICON_SIZE // 2)
            )
        )

    def draw_loot_on_ground(self) -> None:
        self.draw_items_on_ground()
        self.draw_gold_on_ground()

    def draw_items_on_ground(self) -> None:
        for item_info, item_quantity, item_position in self.items[self.current_map_id]:
            item_x, item_y = item_position
            item_position_on_screen = self.map_manager.convert_map_position_to_screen_position(item_x, item_y)
            item_rarity = item_info[ItemsTable.RARITY_ID]
            self._draw_item_glow(item_rarity, item_position_on_screen)
            self.draw_loot_icon(item_position_on_screen)

    def get_gold_icon(self, gold_quantity):
        for icon_index, gold_quantity_range in enumerate(self.GOLD_QUANTITY_RANGES):
            if gold_quantity < gold_quantity_range:
                return self.gold_icons[icon_index]

    def draw_gold_on_ground(self) -> None:
        for gold_quantity, gold_position in self.gold[self.current_map_id]:
            gold_x, gold_y = gold_position
            gold_position_on_screen = self.map_manager.convert_map_position_to_screen_position(gold_x, gold_y)
            self.draw_gold_icon(gold_position_on_screen, self.get_gold_icon(gold_quantity))

    def _draw_hovered_gold_name(self) -> bool:
        for gold_quantity, gold_position in self.gold[self.current_map_id]:
            gold_x, gold_y = gold_position
            gold_name = f'{gold_quantity} gold'
            gold_position_on_screen = self.map_manager.convert_map_position_to_screen_position(gold_x, gold_y)
            if self.is_loot_hovered(gold_position_on_screen, gold_name):
                self._draw_loot_name(
                    loot_name=gold_name,
                    loot_position=gold_position,
                    is_hovered=True
                )
                return True
        return False

    def _draw_hovered_item_name(self) -> bool:
        for item_info, item_quantity, item_position in self.items[self.current_map_id]:
            item_x, item_y = item_position
            item_name_position_on_screen = self.map_manager.convert_map_position_to_screen_position(item_x, item_y)
            if self.is_loot_hovered(item_name_position_on_screen, item_info[ItemsTable.ITEM_NAME]):
                self._draw_loot_name(
                    loot_name=item_info[ItemsTable.ITEM_NAME],
                    loot_position=item_position,
                    loot_rarity=item_info[ItemsTable.RARITY_ID],
                    is_hovered=True
                )
                return True
        return False

    def _draw_hovered_loot_name(self) -> None:
        if self._draw_hovered_item_name():
            return
        self._draw_hovered_gold_name()

    def _draw_gold_name(self, gold_quantity, position, is_hovered=False) -> None:
        pass

    def _draw_loot_name(self, loot_name, loot_position, loot_rarity=RarityType.COMMON, is_hovered=False) -> None:
        if is_hovered:
            text_color = BLACK
            background_color = RARITY_COLORS[loot_rarity]
        else:
            text_color = RARITY_COLORS[loot_rarity]
            background_color = WHITE

        loot_name_text = self.LOOT_NAME_FONT.render(loot_name, True, text_color)
        loot_x, loot_y = loot_position
        loot_screen_x, loot_screen_y = self.map_manager.convert_map_position_to_screen_position(loot_x, loot_y)
        loot_name_x = loot_screen_x - (loot_name_text.get_width() // 2) - self.LOOT_NAME_PADDING_X
        loot_name_y = loot_screen_y - self.LOOT_NAME_OFFSET_Y - loot_name_text.get_height()

        loot_name_rect = pygame.Rect(
            loot_name_x,
            loot_name_y,
            loot_name_text.get_width() + (2 * self.LOOT_NAME_PADDING_X),
            loot_name_text.get_height()
        )

        # draw background
        pygame.draw.rect(
            self.game_surface,
            background_color,
            loot_name_rect,
            border_radius=10
        )

        # draw black border
        pygame.draw.rect(
            self.game_surface,
            BLACK,
            loot_name_rect,
            width=BORDER_WIDTH,
            border_radius=10
        )

        self.game_surface.blit(loot_name_text, (loot_name_x + self.LOOT_NAME_PADDING_X, loot_name_y))

    def _draw_loot_names(self) -> None:
        self._draw_items_names()
        self.draw_gold_names()

    def draw_gold_names(self) -> None:
        for gold_quantity, gold_position in self.gold[self.current_map_id]:
            self._draw_loot_name(
                loot_name=f'{gold_quantity} gold',
                loot_position=gold_position
            )

    def _draw_items_names(self) -> None:
        for item_info, item_quantity, item_position in self.items[self.current_map_id]:
            self._draw_loot_name(
                loot_name=item_info[ItemsTable.ITEM_NAME],
                loot_position=item_position,
                loot_rarity=item_info[ItemsTable.RARITY_ID]
            )

    def draw_loot(self) -> None:
        self.draw_loot_on_ground()
        if self.draw_loot_names:
            self._draw_loot_names()
        self._draw_hovered_loot_name()
