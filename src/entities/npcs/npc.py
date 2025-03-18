from typing import override

from src.colors import RARITY_COLORS, RED, GREEN
from src.common_utils import euclidean_distance
from src.entities.character import Character, CHARACTER_DRAW_SIZE
from src.entities.entity_marker import ENTITY_MARKER_PRIORITIES, EntityMarker
from src.entities.npcs.npc_roles.banker import BankerNpc  # noqa
from src.entities.npcs.npc_roles.quest_giver import QuestGiver  # noqa
from src.entities.npcs.npc_roles.vendor import Vendor  # noqa
from src.enums.character_attribute_type import CharacterAttributeType
from src.enums.character_status_type import CharacterStatusType
from src.enums.cursor_type import CursorType
from src.enums.npc_role_type import NpcRoleType
from src.enums.quote_type import QuoteType
from src.fonts import FONT_ALICE_IN_WONDERLAND_16, FONT_ALICE_IN_WONDERLAND_32
from src.interface.bar import Bar
from src.managers.core.mouse_manager import MouseManager

NPC_CURSOR_NAMES = {
    NpcRoleType.VENDOR: CursorType.VENDOR,
    NpcRoleType.BANKER: CursorType.SELL,
    NpcRoleType.QUEST_GIVER: CursorType.TALK,
    CharacterStatusType.HOSTILE: CursorType.ATTACK
}


class Npc(Character):
    RESPAWN_TIME_IN_SECONDS = 60.0

    ACTIVATION_DISTANCE_HYSTERESIS = 500

    hostile_mini_hp_bar = None
    friendly_mini_hp_bar = None
    MINI_HP_BAR_WIDTH = CHARACTER_DRAW_SIZE
    MINI_HP_BAR_HEIGHT = 10
    MINI_HP_BAR_OFFSET_Y = 20

    def __init__(self, game_surface, map_id, x, y, draw_size, name, sprite_name,
                 attributes, faction, rarity, lvl, roles_names, title=None):
        super().__init__(
            game_surface=game_surface,
            map_id=map_id,
            x=x,
            y=y,
            draw_size=draw_size,
            sprite_name=sprite_name,
            name=name,
            lvl=lvl,
            attributes=attributes,
            faction=faction
        )

        self.rarity = rarity

        self.name_text = FONT_ALICE_IN_WONDERLAND_32.render(self._name, False, RARITY_COLORS[self.rarity])

        self.has_title = title is not None
        if self.has_title:
            self.title_text = FONT_ALICE_IN_WONDERLAND_16.render(title, False, RARITY_COLORS[self.rarity])

        self.spawn_x = self.x
        self.spawn_y = self.y

        self.is_activated = False

        self.set_marker(roles_names)

        self.roles = self.create_roles(roles_names)

    @classmethod
    def initialize_mini_hp_bars(cls, game_surface):
        cls.hostile_mini_hp_bar = Bar(
            game_surface,
            x=0,
            y=0,
            width=cls.MINI_HP_BAR_WIDTH,
            height=cls.MINI_HP_BAR_HEIGHT,
            color=RED,
            border_radius=90
        )
        cls.friendly_mini_hp_bar = Bar(
            game_surface,
            x=0,
            y=0,
            width=cls.MINI_HP_BAR_WIDTH,
            height=cls.MINI_HP_BAR_HEIGHT,
            color=GREEN,
            border_radius=90
        )

    def create_roles(self, roles_names):
        roles = []
        for role_name in roles_names:
            role_class = globals().get(role_name.capitalize())
            if role_class is not None:
                roles.append(role_class(self))
        return roles

    def set_marker(self, roles_names):
        for marker_name, priority in ENTITY_MARKER_PRIORITIES.items():
            if marker_name in roles_names:
                self.marker = EntityMarker(
                    game_surface=self.game_surface,
                    entity_draw_size=self._draw_size,
                    marker_name=marker_name
                )
                return

    def get_cursor_name(self):
        role_name = None
        if self.is_enemy(self.player_manager):
            role_name = CharacterStatusType.HOSTILE
        if len(self.roles) > 0:
            role_name = self.roles[0].get_role_name()

        return NPC_CURSOR_NAMES.get(role_name, CursorType.POINT)

    def handle_respawn(self):
        if self.is_dead:
            if (self.game_clock.game_time - self.death_time) > self.RESPAWN_TIME_IN_SECONDS:
                self.reset()

    @override
    def handle_death(self):
        if self.died_right_now:
            self.set_state_dead()
            if self.is_enemy(self.player_manager):
                self.loot_manager.generate_loot(self.position)
                self.loot_manager.generate_gold(self.position, self._lvl, self.rarity)

    @property
    def is_immune(self):
        return False

    def is_target_in_activation_distance(self, target):
        if target.is_dead or target.is_immune:
            return False
        elif self.is_activated:
            return self.is_target_in_distance(
                target,
                (self.get_attribute(CharacterAttributeType.ACTIVATION_DISTANCE) + self.ACTIVATION_DISTANCE_HYSTERESIS)
            )
        else:
            return self.is_target_in_distance(
                target,
                self.get_attribute(CharacterAttributeType.ACTIVATION_DISTANCE)
            )

    def handle_move_to_target(self, delta_time, target):
        self.find_path(target)
        self.move_to_destination(delta_time)

    def find_path(self, target):
        if not self.is_dead:
            self_row = self.row
            self_column = self.column
            target_row = target.row
            target_column = target.column

            is_activated = self.is_activated
            is_target_in_activation_distance = self.is_target_in_activation_distance(target)
            is_collision_between_fields = self.map_manager.is_collision_between_fields(
                (self_row, self_column),
                (target_row, target_column)
            )

            if not is_activated and is_target_in_activation_distance and not is_collision_between_fields:
                self.is_activated = True
                target_x = target.x
                target_y = target.y
                quote_type = QuoteType.ENEMY if self.is_enemy(target) else QuoteType.NPC
                self.quotes_manager.push_quote_to_queue(quote_type, self, self._draw_size)
            elif is_activated and is_target_in_activation_distance:
                target_x = target.x
                target_y = target.y
            else:
                self.is_activated = False
                target_x = self.spawn_x
                target_y = self.spawn_y
            self.set_path(target_x, target_y)

    @property
    def is_clicked(self):
        return MouseManager.is_left_clicked() and self.is_hovered

    def handle_event(self):
        self.handle_quote()
        self.handle_death()
        self.handle_respawn()
        self.handle_spell_cast_finish()

    def reset(self):
        self.set_state_alive()
        self.death_time = float('-inf')
        self.last_attack_time = float('-inf')
        self.increase_hp(-1)
        self.increase_mana(-1)
        self._x = self.spawn_x
        self._y = self.spawn_y
        self.is_activated = False

    def handle_quote(self):
        pass
        # if self.is_in_distance(self.player_manager.get_position, self.interaction_distance):
        #     if not self.is_activated:
        #         quote_type = QuoteType.ENEMY if self.is_hostile() else QuoteType.NPC
        #         self.quotes_manager.push_quote_to_queue(quote_type, self, self._draw_size)
        #         self.is_activated = True
        # else:
        #     self.is_activated = False

    def get_nearest_target(self):
        nearest_target = None
        nearest_distance = float('inf')
        for npc in self.npcs_manager.npcs[self._map_id]:
            if npc != self and not npc.is_dead:
                distance = euclidean_distance(self.position, npc.position)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_target = npc

        if euclidean_distance(self.position, self.player_manager.position) < nearest_distance:
            nearest_target = self.player_manager

        return nearest_target

    def perform_hostile_actions(self, delta_time):
        target = self.get_nearest_target()
        self.handle_move_to_target(delta_time, target)
        self.perform_attack(target)

    def perform_friendly_actions(self, delta_time):
        pass

    def perform_actions(self, delta_time):
        if self.is_enemy(self.player_manager):
            self.perform_hostile_actions(delta_time)
        else:
            self.perform_friendly_actions(delta_time)

    def interact(self):
        # TODO choose interaction (quest, vendor, bank etc.)
        for role in self.roles:
            role.interact()

    def draw_mini_hp_bar(self) -> None:
        if not self.is_dead:
            screen_position = self.map_manager.convert_map_position_to_screen_position(self.x, self.y)
            draw_x, draw_y = screen_position
            mini_hp_bar_x = draw_x - (self.MINI_HP_BAR_WIDTH // 2)
            mini_hp_bar_y = draw_y - (self._draw_size // 2) - self.MINI_HP_BAR_OFFSET_Y
            if self.is_enemy(self.player_manager):
                self.hostile_mini_hp_bar.set_position(mini_hp_bar_x, mini_hp_bar_y)
                self.hostile_mini_hp_bar.draw(
                    self.attributes[CharacterAttributeType.HP],
                    self.attributes[CharacterAttributeType.MAX_HP]
                )
            else:
                self.friendly_mini_hp_bar.set_position(mini_hp_bar_x, mini_hp_bar_y)
                self.friendly_mini_hp_bar.draw(
                    self.attributes[CharacterAttributeType.HP],
                    self.attributes[CharacterAttributeType.MAX_HP]
                )
