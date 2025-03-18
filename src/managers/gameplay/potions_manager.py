import pygame.image

from src.enums.character_attribute_type import CharacterAttributeType
from src.enums.error_message_type import ErrorMessageType
from src.interface.button import Button
from src.interface.interface_constants import LOWER_UI_BAR_HEIGHT, MINI_BARS_X, MINI_BARS_WIDTH
from src.paths import PATH_IMAGE_HP_POTION, PATH_IMAGE_MANA_POTION


class PotionsManager:
    _instance = None

    POTIONS_OFFSET_X = MINI_BARS_X + (2 * MINI_BARS_WIDTH)
    POTION_TILE_SIZE = 40

    POTION_COOLDOWN_TIME_IN_SECONDS = 30.0

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

            self.game_clock = None
            self.player_manager = None
            self.error_messages_manager = None

            self.game_surface = game_surface

            self.hp_potion_last_use_time = float('-inf')
            self.mana_potion_last_use_time = float('-inf')

            self.hp_potion_image = pygame.image.load(PATH_IMAGE_HP_POTION).convert_alpha()
            self.hp_potion_image = pygame.transform.scale(
                self.hp_potion_image,
                (
                    self.POTION_TILE_SIZE,
                    self.POTION_TILE_SIZE
                )
            )

            self.health_potion_button = Button(
                game_surface=game_surface,
                center_x=self.POTIONS_OFFSET_X,
                center_y=self.game_surface.get_height() - (LOWER_UI_BAR_HEIGHT // 2),
                image=self.hp_potion_image,
                action=self.use_hp_potion,
                is_ready_check=self._is_hp_potion_ready
            )

            self.mana_potion_image = pygame.image.load(PATH_IMAGE_MANA_POTION).convert_alpha()
            self.mana_potion_image = pygame.transform.scale(
                self.mana_potion_image,
                (
                    self.POTION_TILE_SIZE,
                    self.POTION_TILE_SIZE
                )
            )

            self.mana_potion_button = Button(
                game_surface=game_surface,
                center_x=self.POTIONS_OFFSET_X + self.POTION_TILE_SIZE + (self.POTION_TILE_SIZE // 2),
                center_y=self.game_surface.get_height() - (LOWER_UI_BAR_HEIGHT // 2),
                image=self.mana_potion_image,
                action=self.use_mana_potion,
                is_ready_check=self._is_mana_potion_ready
            )

    def setup_references(self) -> None:
        from src.managers.gameplay.player_manager import PlayerManager
        from src.managers.ui.error_messages_manager import ErrorMessagesManager
        from src.game_clock import GameClock

        self.game_clock = GameClock.get_instance()
        self.player_manager = PlayerManager.get_instance()
        self.error_messages_manager = ErrorMessagesManager.get_instance()

    def _is_hp_potion_ready(self) -> bool:
        return (self.game_clock.game_time - self.hp_potion_last_use_time) > self.POTION_COOLDOWN_TIME_IN_SECONDS

    def _is_mana_potion_ready(self) -> bool:
        return (self.game_clock.game_time - self.mana_potion_last_use_time) > self.POTION_COOLDOWN_TIME_IN_SECONDS

    def use_mana_potion(self) -> None:
        if self.player_manager.is_dead:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.YOU_ARE_DEAD)
        elif not self._is_mana_potion_ready:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.NOT_READY_YET)
        elif self.player_manager.get_attribute(CharacterAttributeType.MANA) == self.player_manager.get_attribute(
                CharacterAttributeType.MAX_MANA):
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.MANA_IS_FULL)
        else:
            self.mana_potion_last_use_time = self.game_clock.game_time
            self.player_manager.attributes[CharacterAttributeType.MANA] = self.player_manager.attributes[
                CharacterAttributeType.MAX_MANA]

    def use_hp_potion(self) -> None:
        if self.player_manager.is_dead:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.YOU_ARE_DEAD)
        elif not self._is_hp_potion_ready:
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.NOT_READY_YET)
        elif self.player_manager.get_attribute(CharacterAttributeType.HP) == self.player_manager.get_attribute(
                CharacterAttributeType.MAX_HP):
            self.error_messages_manager.push_message_to_queue(ErrorMessageType.HEALTH_IS_FULL)
        else:
            self.hp_potion_last_use_time = self.game_clock.game_time
            self.player_manager.attributes[CharacterAttributeType.HP] = self.player_manager.attributes[
                CharacterAttributeType.MAX_HP]

    def handle_mouse_events(self) -> bool:
        if self.health_potion_button.handle_event():
            return True
        if self.mana_potion_button.handle_event():
            return True
        return False

    def reset_cooldowns(self) -> None:
        self.hp_potion_last_use_time = float('-inf')
        self.mana_potion_last_use_time = float('-inf')

    def draw_potions(self) -> None:
        self.health_potion_button.draw()
        self.mana_potion_button.draw()
