import pygame

from src.common_utils import euclidean_distance
from src.managers.core.mouse_manager import MouseManager


class Entity:
    map_manager = None
    loot_manager = None
    quotes_manager = None
    bank_manager = None
    vendor_manager = None
    npcs_manager = None
    interface_manager = None
    interactive_objects_manager = None
    player_manager = None
    game_clock = None

    def __init__(self, game_surface, map_id, x, y, draw_size, name):
        self.game_surface = game_surface

        self._map_id = map_id
        self._x = x
        self._y = y

        self._name = name

        self._draw_size = draw_size
        self.animated_sprite = None
        self.marker = None

        self.interaction_distance = self._draw_size

    @classmethod
    def setup_references(cls):
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.gameplay.loot_manager import LootManager
        from src.managers.gameplay.quotes_manager import QuotesManager
        from src.managers.gameplay.bank_manager import BankManager
        from src.managers.gameplay.vendor_manager import VendorManager
        from src.managers.gameplay.npcs_manager import NpcsManager
        from src.managers.ui.interface_manager import InterfaceManager
        from src.managers.gameplay.interactive_objects_manager import InteractiveObjectsManager
        from src.managers.gameplay.player_manager import PlayerManager
        from src.game_clock import GameClock

        cls.game_clock = GameClock.get_instance()
        cls.map_manager = MapManager.get_instance()
        cls.loot_manager = LootManager.get_instance()
        cls.quotes_manager = QuotesManager.get_instance()
        cls.bank_manager = BankManager.get_instance()
        cls.vendor_manager = VendorManager.get_instance()
        cls.npcs_manager = NpcsManager.get_instance()
        cls.interface_manager = InterfaceManager.get_instance()
        cls.interactive_objects_manager = InteractiveObjectsManager.get_instance()
        cls.player_manager = PlayerManager.get_instance()

    @property
    def name(self):
        return self._name

    @property
    def map_id(self):
        return self._map_id

    def set_map_id(self, map_id):
        self._map_id = map_id

    @property
    def position(self) -> [int, int]:
        return self._x, self._y

    def set_position(self, x, y) -> None:
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def row(self):
        return self.map_manager.get_row(self._y)

    @property
    def column(self):
        return self.map_manager.get_column(self._x)

    @property
    def draw_size(self):
        return self._draw_size

    @property
    def is_hovered(self) -> bool:
        collide_rect = pygame.Rect(
            self._x - (self._draw_size // 2),
            self._y - (self._draw_size // 2),
            self._draw_size,
            self._draw_size
        )
        return collide_rect.collidepoint(self.map_manager.convert_screen_position_to_map_position())

    @property
    def is_clicked(self):
        return MouseManager.is_left_clicked() and self.is_hovered

    def is_target_in_distance(self, target, distance):
        return euclidean_distance((self._x, self._y), target.position) <= distance

    def is_target_in_interaction_distance(self, target):
        return euclidean_distance((self._x, self._y), target.position) <= self.interaction_distance

    def draw(self):
        if self.map_manager.map_id == self._map_id:
            position_on_screen = self.map_manager.convert_map_position_to_screen_position(self.x, self.y)
            if self.animated_sprite is not None:
                self.animated_sprite.draw(position_on_screen)
            if self.marker is not None:
                self.marker.draw_entity_marker(position_on_screen)
