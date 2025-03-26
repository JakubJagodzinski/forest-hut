from typing import override

import pygame

from database.game_database_table_columns_names import CharactersTable, CharacterPositionsTable
from src.colors import SEA_BLUE
from src.entities.character import Character, CHARACTER_DRAW_SIZE
from src.enums.character_attribute_type import CharacterAttributeType
from src.enums.character_status_type import CharacterStatusType
from src.enums.chat_message_color_type import ChatMessageColorType
from src.enums.move_direction_type import MoveDirection
from src.enums.sound_type import SoundType
from src.enums.sprite_state import SpriteState
from src.interface.bar import Bar
from src.managers.core.mouse_manager import MouseManager
from src.managers.gameplay.map_manager import TOWN_MAP_ID
from src.spells.town_portal_spell import OpenPortalToTownSpell


class PlayerManager(Character):
    _instance = None

    XP_PER_LEVEL = 1_000
    HP_PER_LVL = 50
    MANA_PER_LVL = 25
    STAMINA_PER_LVL = 10

    RESURRECT_IMMUNE_TIME_IN_SECONDS = 5.0

    RUN_SPEED_STAMINA_DECREASE_PER_PIXEL = 1

    CASTING_BAR_WIDTH = CHARACTER_DRAW_SIZE
    CASTING_BAR_HEIGHT = 10
    CASTING_BAR_OFFSET_Y = 20

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_surface, character_id, character_name):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            self.game_surface = game_surface
            self._character_id = character_id
            self.character_name = character_name

            self.game_clock = None
            self.map_manager = None
            self.quotes_manager = None
            self.sound_manager = None
            self.chat_manager = None
            self.enemies_manager = None
            self.error_messages_manager = None
            self.loot_manager = None
            self.potions_manager = None
            self.inventory_manager = None
            self.kill_series_manager = None
            self.npcs_manager = None
            self.interactive_objects_manager = None

            from src.database_service import DatabaseService

            self.character_data = DatabaseService.get_character_data(self._character_id)
            self.is_hardcore = self.character_data[CharactersTable.IS_HARDCORE]
            self._xp = self.character_data[CharactersTable.XP]

            character_position = DatabaseService.get_character_position(self._character_id)
            attributes = DatabaseService.get_character_attributes(self._character_id)
            faction = DatabaseService.get_faction_name(self.character_data[CharactersTable.FACTION_ID])

            super().__init__(
                game_surface=game_surface,
                map_id=character_position[CharacterPositionsTable.MAP_ID],
                x=character_position[CharacterPositionsTable.X],
                y=character_position[CharacterPositionsTable.Y],
                draw_size=CHARACTER_DRAW_SIZE,
                sprite_name='necromancer',
                name=self.character_data[CharactersTable.CHARACTER_NAME],
                lvl=self.character_data[CharactersTable.LVL],
                attributes=attributes,
                faction=faction,
                status=CharacterStatusType.FRIENDLY
            )

            self._draw_position = (
                self.game_surface.get_width() // 2,
                self.game_surface.get_height() // 2
            )

            self.open_portal_to_town_spell = OpenPortalToTownSpell(
                caster_reference=self
            )

            self.portal_to_town = None
            self.portal_in_town = None

            casting_bar_x = (self.game_surface.get_width() // 2) - (self.CASTING_BAR_WIDTH // 2)
            casting_bar_y = ((self.game_surface.get_height() // 2)
                             - (CHARACTER_DRAW_SIZE // 2)
                             - self.CASTING_BAR_OFFSET_Y)
            self.casting_bar = Bar(
                self.game_surface,
                x=casting_bar_x,
                y=casting_bar_y,
                width=self.CASTING_BAR_WIDTH,
                height=self.CASTING_BAR_HEIGHT,
                color=SEA_BLUE,
                is_fill_complement=True,
                border_radius=90
            )

            self.last_regeneration_time = float('-inf')
            self.immune_start_time = float('-inf')
            self.is_exhausted = False

    def setup_references(self):
        from src.managers.gameplay.quotes_manager import QuotesManager
        from src.managers.gameplay.loot_manager import LootManager
        from src.managers.gameplay.potions_manager import PotionsManager
        from src.managers.ui.chat_manager import ChatManager
        from src.managers.ui.error_messages_manager import ErrorMessagesManager
        from src.managers.gameplay.inventory_manager import InventoryManager
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.core.sound_manager import SoundManager
        from src.managers.gameplay.kill_series_manager import KillSeriesManager
        from src.managers.gameplay.npcs_manager import NpcsManager
        from src.managers.gameplay.interactive_objects_manager import InteractiveObjectsManager
        from src.game_clock import GameClock

        self.game_clock = GameClock.get_instance()
        self.interactive_objects_manager = InteractiveObjectsManager.get_instance()
        self.npcs_manager = NpcsManager.get_instance()
        self.kill_series_manager = KillSeriesManager.get_instance()
        self.inventory_manager = InventoryManager.get_instance()
        self.sound_manager = SoundManager.get_instance()
        self.quotes_manager = QuotesManager.get_instance()
        self.map_manager = MapManager.get_instance()
        self.chat_manager = ChatManager.get_instance()
        self.error_messages_manager = ErrorMessagesManager.get_instance()
        self.loot_manager = LootManager.get_instance()
        self.potions_manager = PotionsManager.get_instance()

    def load_spells(self):
        super().load_spells()
        self.spells_handler.add_spell(self.open_portal_to_town_spell)

    @property
    def character_id(self):
        return self._character_id

    @property
    def draw_position(self):
        return self._draw_position

    @property
    def is_in_town(self) -> bool:
        return self.map_id == TOWN_MAP_ID

    @property
    def is_immune(self):
        return (self.game_clock.game_time - self.immune_start_time) < self.RESURRECT_IMMUNE_TIME_IN_SECONDS

    @property
    def is_regeneration_ready(self):
        return (self.game_clock.game_time - self.last_regeneration_time) > 1.0

    @property
    def xp(self) -> int:
        return self._xp

    @property
    def required_xp(self) -> int:
        return self._lvl * self.XP_PER_LEVEL

    def resurrect_in_town(self):
        self.fully_regenerate()
        self.portal_to_town.final_action()

    def resurrect_here(self):
        self.immune_start_time = self.game_clock.game_time
        self.fully_regenerate()

    def fully_regenerate(self) -> None:
        self.increase_hp(self.attributes[CharacterAttributeType.MAX_HP])
        self.increase_mana(self.attributes[CharacterAttributeType.MAX_MANA])
        self.increase_stamina(self.attributes[CharacterAttributeType.MAX_STAMINA])
        self.is_exhausted = False
        self.potions_manager.reset_cooldowns()

    @override
    def handle_death(self):
        if self.died_right_now:
            self.set_state_dead()
            self.inventory_manager.put_held_item_back_to_inventory()
            if self.is_hardcore:
                death_message = f'Hardcore player {self.character_name} died forever!'
            else:
                death_message = f'{self.character_name} died!'
            self.chat_manager.push_message_to_chat(death_message, ChatMessageColorType.PLAYER_DEATH)
            self.sound_manager.play_sound(SoundType.GAME_OVER)

    def handle_regeneration(self) -> None:
        if not self.is_dead and not self.is_in_combat and self.is_regeneration_ready:
            self.last_regeneration_time = self.game_clock.game_time
            self.increase_hp(self.attributes[CharacterAttributeType.HP_REGENERATION_RATE])
            self.increase_mana(self.attributes[CharacterAttributeType.MANA_REGENERATION_RATE])
            self.increase_stamina(self.attributes[CharacterAttributeType.STAMINA_REGENERATION_RATE])

    def increase_xp(self, amount) -> None:
        self._xp += amount
        if self._xp >= self.required_xp:
            self.handle_level_up()

    def add_gold(self, amount: int) -> None:
        self.inventory_manager.add_gold(amount)

    def handle_kill_series_end(self) -> None:
        xp_bonus = self.kill_series_manager.handle_kill_series_end()
        self.increase_xp(xp_bonus)

    def handle_enemy_killed(self, enemies_killed: int) -> None:
        if enemies_killed > 0:
            self.kill_series_manager.increment_kill_series(enemies_killed)
            self.increase_xp(enemies_killed)

    def handle_level_up(self) -> None:
        remaining_xp = (self._xp % self.required_xp)
        self._lvl += int(self._xp // self.required_xp)
        self.attributes[CharacterAttributeType.MAX_HP] += self.HP_PER_LVL
        self.attributes[CharacterAttributeType.MAX_MANA] += self.MANA_PER_LVL
        self.attributes[CharacterAttributeType.MAX_STAMINA] += self.STAMINA_PER_LVL
        self._xp = remaining_xp
        self.fully_regenerate()
        self.sound_manager.play_sound(SoundType.LEVEL_UP)
        self.interface_manager.set_level_text()

    def increase_stamina(self, delta: int) -> None:
        if delta == -1:
            delta = self.get_attribute(CharacterAttributeType.MAX_STAMINA)
        self.attributes[CharacterAttributeType.STAMINA] = min(
            self.get_attribute(CharacterAttributeType.STAMINA) + delta,
            self.get_attribute(CharacterAttributeType.MAX_STAMINA)
        )
        if self.get_attribute(CharacterAttributeType.STAMINA) == self.get_attribute(
                CharacterAttributeType.MAX_STAMINA):
            self.is_exhausted = False

    def decrease_stamina(self, delta: int) -> None:
        self.attributes[CharacterAttributeType.STAMINA] = max(
            self.get_attribute(CharacterAttributeType.STAMINA) - delta,
            0
        )
        if self.get_attribute(CharacterAttributeType.STAMINA) == 0:
            self.is_exhausted = True

    @property
    def is_sprint_available(self) -> bool:
        return (not self.is_exhausted
                and self.get_attribute(CharacterAttributeType.STAMINA) >= self.RUN_SPEED_STAMINA_DECREASE_PER_PIXEL)

    def handle_set_destination_path(self):
        if MouseManager.is_left_clicked():
            clicked_x, clicked_y = self.map_manager.convert_screen_position_to_map_position()
            self.set_path(clicked_x, clicked_y)

    def handle_move(self, delta_time: float) -> None:
        start_x, start_y = self.x, self.y
        movement_vector = [0, 0]
        keyboard_move_handled = False

        if not self.chat_manager.is_input_box_active():
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.is_sprint_available:
                self.set_movement_speed(self.SPEED_RUN)
            else:
                self.set_movement_speed(self.SPEED_WALK)

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                keyboard_move_handled = True
                movement_vector[1] = -1
                self.animated_sprite.set_direction(MoveDirection.UP)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                keyboard_move_handled = True
                movement_vector[1] = 1
                self.animated_sprite.set_direction(MoveDirection.DOWN)

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                keyboard_move_handled = True
                movement_vector[0] = -1
                self.animated_sprite.set_direction(MoveDirection.LEFT)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                keyboard_move_handled = True
                movement_vector[0] = 1
                self.animated_sprite.set_direction(MoveDirection.RIGHT)

            if keys[pygame.K_LCTRL]:
                keyboard_move_handled = False

        if keyboard_move_handled:
            self.is_moving_to_destination_row_and_column = False
            self.move(movement_vector, delta_time)
        else:
            self.animated_sprite.set_sprite_state(SpriteState.IDLE)

        if self.is_moving_to_destination_row_and_column:
            self.move_to_destination(delta_time)

        if self.movement_speed == self.SPEED_RUN and (self.x != start_x or self.y != start_y):
            self.decrease_stamina(self.RUN_SPEED_STAMINA_DECREASE_PER_PIXEL)

    def handle_mouse_events(self) -> bool:
        if self.handle_attack_npc():
            return True
        if self.handle_gold_pickup():
            return True
        if self.handle_item_pickup():
            return True
        if self.handle_interact_with_npc():
            return True
        if self.handle_interact_with_object():
            return True
        if self.handle_portals_events():
            return True
        if self.handle_set_destination_path():
            return True
        return False

    def handle_attack_npc(self) -> bool:
        for npc in self.npcs_manager.npcs[self.map_manager.map_id]:
            if npc.is_clicked:
                if self.perform_attack(npc):
                    self.kill_series_manager.refresh_kill_series()
                    if npc.died_right_now:
                        self.handle_enemy_killed(1)
                    return True
        return False

    def handle_gold_pickup(self) -> bool:
        gold_and_position = self.loot_manager.pick_gold_up(self.position)
        if gold_and_position is not None:
            gold_quantity, picked_gold_position = gold_and_position
            self.inventory_manager.add_gold(gold_quantity)
            self.set_sprite_direction_to_position(picked_gold_position)
            return True
        else:
            return False

    def handle_item_pickup(self) -> bool:
        item_and_position = self.loot_manager.pick_item_up(self.position)
        if item_and_position is not None:
            picked_item, picked_item_position = item_and_position
            item_info, item_quantity = picked_item
            self.inventory_manager.add_item_to_inventory(item_info, item_quantity)
            self.set_sprite_direction_to_position(picked_item_position)
            return True
        else:
            return False

    def handle_interact_with_npc(self) -> bool:
        for npc in self.npcs_manager.npcs[self._map_id]:
            if npc.is_clicked and not self.is_enemy(npc) and self.is_target_in_interaction_distance(npc):
                npc.interact()
                return True
        return False

    def handle_interact_with_object(self) -> bool:
        for interactive_object in self.interactive_objects_manager.interactive_objects[self._map_id]:
            if (interactive_object.is_clicked
                    and interactive_object.is_active
                    and self.is_target_in_interaction_distance(interactive_object)):
                interactive_object.interact()
                return True
        return False

    def handle_portals_events(self) -> bool:
        if (self.portal_to_town is not None
                and self.portal_to_town.is_clicked
                and self.is_target_in_interaction_distance(self.portal_to_town)):
            self.portal_to_town.interact()
            return True
        if (self.portal_in_town is not None
                and self.portal_in_town.is_clicked
                and self.is_target_in_interaction_distance(self.portal_in_town)):
            self.portal_in_town.interact()
            return True
        return False

    def draw_portals(self):
        if self.portal_to_town:
            self.portal_to_town.draw()

        if self.portal_in_town:
            self.portal_in_town.draw()

    def draw_player(self) -> None:
        self.draw_portals()
        self.spells_handler.draw_casting_animation()
        self.animated_sprite.draw(self._draw_position)
