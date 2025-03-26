import pygame

from database.game_database_table_columns_names import NpcsTable, MapNpcPositionsTable
from src.colors import GREEN, RED, WHITE
from src.entities.character import CHARACTER_DRAW_SIZE
from src.entities.npcs.npc import Npc
from src.enums.character_attribute_type import CharacterAttributeType
from src.enums.chat_message_color_type import ChatMessageColorType
from src.fonts import FONT_ARIAL_16
from src.interface.bar import Bar
from src.keybindings import KEY_SWITCH_SHOW_FRIENDLY_NPC_MINI_HP_BARS, KEY_SWITCH_SHOW_HOSTILE_NPC_MINI_HP_BARS


class NpcsManager:
    _instance = None

    BACKGROUND_BORDER_NAME_TEXT_OFFSET_X = 20

    NPC_NAME_Y = 10
    NPC_TITLE_Y = 50

    NPC_HP_BAR_Y = 75
    NPC_HP_BAR_WIDTH = 200
    NPC_HP_BAR_HEIGHT = 15

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_surface):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            self.game_surface = game_surface

            self.map_manager = None
            self.chat_manager = None
            self.player_manager = None
            self.loot_manager = None

            self.npcs = {}

            self.hp_bar_x = (self.game_surface.get_width() // 2) - (self.NPC_HP_BAR_WIDTH // 2)
            self.hp_bar_y = self.NPC_HP_BAR_Y
            self.npc_hp_bar = Bar(
                self.game_surface,
                x=self.hp_bar_x,
                y=self.hp_bar_y,
                width=self.NPC_HP_BAR_WIDTH,
                height=self.NPC_HP_BAR_HEIGHT,
                color=RED,
                border_radius=90
            )
            self.npc_hp_font = FONT_ARIAL_16

            self.are_hostile_npc_mini_hp_bar_visible = False
            self.are_friendly_npc_mini_hp_bar_visible = False

            self.hovered_npc = None

    def setup_references(self):
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.ui.chat_manager import ChatManager
        from src.managers.gameplay.loot_manager import LootManager
        from src.managers.gameplay.player_manager import PlayerManager

        self.map_manager = MapManager.get_instance()
        self.chat_manager = ChatManager.get_instance()
        self.player_manager = PlayerManager.get_instance()
        self.loot_manager = LootManager.get_instance()

    def update(self):
        self.load_npcs()

    def load_npcs(self) -> None:
        current_map_id = self.map_manager.map_id
        if current_map_id not in self.npcs:
            self.npcs[current_map_id] = []
            from src.database_service import DatabaseService
            npc_positions_on_map = DatabaseService.get_map_npc_positions(current_map_id)
            npc_ids = {npc[NpcsTable.NPC_ID] for npc in npc_positions_on_map}
            loaded_npcs = DatabaseService.get_npcs_by_ids(npc_ids)
            for npc_position_on_map in npc_positions_on_map:
                npc_id = npc_position_on_map[NpcsTable.NPC_ID]
                npc_data = None
                for npc in loaded_npcs:
                    if npc[NpcsTable.NPC_ID] == npc_id:
                        npc_data = npc
                        break

                npc_attributes = DatabaseService.get_npc_attributes(npc_id)
                npc_roles_names = DatabaseService.get_npc_roles_names(npc_id)

                self.npcs[current_map_id].append(
                    Npc(
                        game_surface=self.game_surface,
                        map_id=current_map_id,
                        x=npc_position_on_map[MapNpcPositionsTable.X],
                        y=npc_position_on_map[MapNpcPositionsTable.Y],
                        draw_size=CHARACTER_DRAW_SIZE,
                        sprite_name=npc_data[NpcsTable.SPRITE_NAME],
                        name=npc_data[NpcsTable.NPC_NAME],
                        attributes=npc_attributes,
                        faction=npc_data[NpcsTable.FACTION_ID],
                        rarity=DatabaseService.get_rarity_by_id(npc_data[NpcsTable.RARITY_ID]),
                        lvl=npc_data[NpcsTable.LVL],
                        roles_names=npc_roles_names,
                        status=npc_data[NpcsTable.STATUS_ID]
                    )
                )

    def handle_events(self) -> bool:
        for npc in self.npcs[self.map_manager.map_id]:
            if npc.handle_event():
                return True
        return False

    def reset_npcs(self) -> None:
        for npc in self.npcs[self.map_manager.map_id]:
            npc.reset()

    def perform_actions(self, delta_time) -> None:
        for npc in self.npcs[self.map_manager.map_id]:
            npc.perform_actions(delta_time)

    def switch_show_hostile_npc_mini_hp_bars(self) -> None:
        self.are_hostile_npc_mini_hp_bar_visible = not self.are_hostile_npc_mini_hp_bar_visible
        state = 'on' if self.are_hostile_npc_mini_hp_bar_visible else 'off'
        self.chat_manager.push_message_to_chat(
            f'Enemies hp bars are now turned {state} [{chr(KEY_SWITCH_SHOW_HOSTILE_NPC_MINI_HP_BARS)}]',
            ChatMessageColorType.SYSTEM
        )

    def switch_show_friendly_npc_mini_hp_bars(self) -> None:
        self.are_friendly_npc_mini_hp_bar_visible = not self.are_friendly_npc_mini_hp_bar_visible
        state = 'on' if self.are_friendly_npc_mini_hp_bar_visible else 'off'
        self.chat_manager.push_message_to_chat(
            f'Friendly npcs hp bars are now turned {state} [{chr(KEY_SWITCH_SHOW_FRIENDLY_NPC_MINI_HP_BARS)}]',
            ChatMessageColorType.SYSTEM
        )

    def draw_npc_info(self, npc):
        if not npc.is_dead and npc.is_hovered:
            npc_name_text_x = (self.game_surface.get_width() // 2) - (npc.name_text.get_width() // 2)
            npc_name_background_x = npc_name_text_x - self.BACKGROUND_BORDER_NAME_TEXT_OFFSET_X
            npc_name_background_width = (npc.name_text.get_width()
                                         + (2 * self.BACKGROUND_BORDER_NAME_TEXT_OFFSET_X))

            background_color = RED if npc.is_enemy(self.player_manager) else GREEN

            # draw background
            pygame.draw.rect(
                self.game_surface,
                background_color,
                (npc_name_background_x,
                 self.NPC_NAME_Y,
                 npc_name_background_width,
                 npc.name_text.get_height()),
                border_radius=90
            )

            # draw npc name
            self.game_surface.blit(npc.name_text, (npc_name_text_x, self.NPC_NAME_Y))

            # draw npc title
            if npc.has_title:
                npc_title_text_x = (self.game_surface.get_width() // 2) - (npc.title_text.get_width() // 2)
                self.game_surface.blit(npc.title_text, (npc_title_text_x, self.NPC_TITLE_Y))

            npc_hp = npc.get_attribute(CharacterAttributeType.HP)
            npc_max_hp = npc.get_attribute(CharacterAttributeType.MAX_HP)

            # draw hp bar
            self.npc_hp_bar.draw(npc_hp, npc_max_hp)

            # draw hp text
            npc_hp_text = self.npc_hp_font.render(f'{npc_hp} / {npc_max_hp}', True, WHITE)
            npc_hp_text_x = (self.hp_bar_x
                             + (self.NPC_HP_BAR_WIDTH // 2)
                             - (npc_hp_text.get_width() // 2))
            npc_hp_text_y = (self.hp_bar_y
                             + (self.NPC_HP_BAR_HEIGHT // 2)
                             - (npc_hp_text.get_height() // 2))
            self.game_surface.blit(npc_hp_text, (npc_hp_text_x, npc_hp_text_y))

    def draw_hovered_npc_info(self) -> None:
        if self.hovered_npc is not None:
            self.draw_npc_info(self.hovered_npc)

    def get_hovered_npc_info(self):
        for npc in self.npcs[self.map_manager.map_id]:
            if not npc.is_dead and npc.is_hovered:
                self.hovered_npc = npc
                return npc.get_cursor_name()
        self.hovered_npc = None
        return None

    def draw_npcs(self) -> None:
        for npc in self.npcs[self.map_manager.map_id]:
            npc.draw()
            if ((self.are_friendly_npc_mini_hp_bar_visible and not self.player_manager.is_enemy(npc))
                    or (self.are_hostile_npc_mini_hp_bar_visible and self.player_manager.is_enemy(npc))):
                npc.draw_mini_hp_bar()
