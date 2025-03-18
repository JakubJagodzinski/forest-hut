import heapq
import os

import pygame

from database.game_database_table_columns_names import MapsTable
from src.colors import WHITE, RED, BLACK
from src.common_utils import manhattan_distance, normalize_value
from src.fonts import FONT_MONOSPACE_COURIER_16
from src.paths import DIR_DATABASE_MAPS, TXT_COLLISIONS_GRID, DIR_ASSETS_MAP_LOADING_SCREENS

MAP_COLLISION_TILE = 50
TOWN_MAP_ID = 2


class MapManager:
    _instance = None

    MAP_SCALE = 4

    AVAILABLE_MOVE_DIRECTIONS = [
        (-1, 0),  # UP
        (1, 0),  # DOWN
        (0, -1),  # LEFT
        (0, 1)  # RIGHT
    ]

    NIGHT_OVERLAY_ALPHA_MIN = 0
    NIGHT_OVERLAY_ALPHA_MAX = 220
    NIGHT_OVERLAY_ACCURACY = 0.2

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

            self.game_context = None
            self.interface_manager = None
            self.player_manager = None
            self.datetime_manager = None

            self.map_id = None
            self.map_info = {}
            self._map_image = None
            self._collisions_grid = []
            self.columns = 0
            self.rows = 0

            self._loading_image = None

            self.night_overlays = []
            overlays_count = int(self.NIGHT_OVERLAY_ALPHA_MAX * self.NIGHT_OVERLAY_ACCURACY) + 1
            alpha_range = (self.NIGHT_OVERLAY_ALPHA_MAX / overlays_count)

            for i in range(overlays_count):
                night_overlay = pygame.Surface((game_surface.get_width(), game_surface.get_height()))
                night_overlay.fill(BLACK)
                night_overlay.set_alpha(int(i * alpha_range))
                self.night_overlays.append(night_overlay)

    def setup_references(self):
        from src.managers.gameplay.player_manager import PlayerManager
        from src.managers.ui.interface_manager import InterfaceManager
        from src.game_context import GameContext
        from src.managers.gameplay.datetime_manager import DatetimeManager

        self.datetime_manager = DatetimeManager.get_instance()
        self.game_context = GameContext.get_instance()
        self.interface_manager = InterfaceManager.get_instance()
        self.player_manager = PlayerManager.get_instance()

    def load_collisions_grid(self):
        with open(os.path.join(DIR_DATABASE_MAPS, f'{self.map_id}', TXT_COLLISIONS_GRID)) as collisions_grid_file:
            self._collisions_grid = []
            for line in collisions_grid_file.readlines():
                line = line.replace('\n', '')
                row = []
                for column in line:
                    row.append(True if column == '#' else False)
                self._collisions_grid.append(row)
            self.rows = len(self._collisions_grid)
            self.columns = len(self._collisions_grid[0])

    def load_map(self, map_id: int) -> None:
        self.map_id = map_id
        from src.database_service import DatabaseService
        self.map_info = DatabaseService.get_map_info(self.map_id)
        self._map_image = pygame.image.load(os.path.join(DIR_DATABASE_MAPS, f'{map_id}', f'{map_id}.png')).convert()
        self._map_image = pygame.transform.scale(
            self._map_image,
            (
                self._map_image.get_width() * self.MAP_SCALE,
                self._map_image.get_height() * self.MAP_SCALE
            )
        )
        self.load_collisions_grid()
        self._loading_image = pygame.image.load(
            os.path.join(DIR_ASSETS_MAP_LOADING_SCREENS, f'{self.map_id}.png')
        ).convert()
        self._loading_image = pygame.transform.scale(self._loading_image, self.game_surface.get_size())
        self.interface_manager.set_location_name_text()
        # self._show_loading_screen()

    @staticmethod
    def get_row(y) -> int:
        return int(y // MAP_COLLISION_TILE)

    @staticmethod
    def get_column(x) -> int:
        return int(x // MAP_COLLISION_TILE)

    def get_map_id(self) -> int:
        return self.map_id

    def get_location_name(self) -> str:
        return self.map_info[MapsTable.MAP_NAME]

    def get_min_lvl(self) -> int:
        return self.map_info[MapsTable.MIN_LVL]

    def get_max_lvl(self) -> int:
        return self.map_info[MapsTable.MAX_LVL]

    def get_location_name_with_levels(self) -> str:
        return f'{self.get_location_name().upper()} ({self.get_min_lvl()}-{self.get_max_lvl()})'

    def convert_screen_position_to_map_position(self) -> [int, int]:
        player_x, player_y = self.player_manager.position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_middle_x = self.game_surface.get_width() // 2
        screen_middle_y = self.game_surface.get_height() // 2
        map_x = player_x - screen_middle_x + mouse_x
        map_y = player_y - screen_middle_y + mouse_y
        return map_x, map_y

    def convert_map_position_to_screen_position(self, x, y) -> [int, int]:
        player_x, player_y = self.player_manager.position
        screen_middle_x = (self.game_surface.get_width() // 2)
        screen_middle_y = (self.game_surface.get_height() // 2)
        map_0_x_screen_position = 0 - player_x + screen_middle_x
        map_0_y_screen_position = 0 - player_y + screen_middle_y
        screen_x = map_0_x_screen_position + x
        screen_y = map_0_y_screen_position + y
        return screen_x, screen_y

    def is_collision_on_field(self, row: int, column: int) -> bool:
        if (0 <= row < self.rows) and (0 <= column < self.columns):
            return self._collisions_grid[row][column]
        else:
            return True

    def is_collision_between_fields(self, field_a, field_b) -> bool:
        row_a, column_a = field_a
        row_b, column_b = field_b
        d_column = abs(column_b - column_a)
        d_row = abs(row_b - row_a)
        sx = 1 if column_a < column_b else -1
        sy = 1 if row_a < row_b else -1
        err = d_column - d_row
        while True:
            if self._collisions_grid[row_a][column_a] == 1:
                return True
            if column_a == column_b and row_a == row_b:
                break
            e2 = 2 * err
            if e2 > -d_row:
                err -= d_row
                column_a += sx
            if e2 < d_column:
                err += d_column
                row_a += sy
        return False

    def a_star(self, start_row: int, start_column: int, destination_row: int, destination_column: int):
        def get_neighbor_fields(row, column):
            return [(row + next_row, column + next_column) for next_row, next_column in self.AVAILABLE_MOVE_DIRECTIONS
                    if not self.is_collision_on_field(row + next_row, column + next_column)]

        def find_nearest_destination_field_without_collision(destination):
            if not self.is_collision_on_field(*destination):
                return destination

            # BFS to find the closest valid position
            visited = set()
            queue = [(destination_row, destination_column)]
            while queue:
                current_field = queue.pop(0)
                for neighbor in get_neighbor_fields(*current_field):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        if not self.is_collision_on_field(neighbor[0], neighbor[1]):
                            return neighbor  # Found the closest valid position
            return None

        destination_field = find_nearest_destination_field_without_collision((destination_row, destination_column))
        if not destination_field:
            return None

        open_set = [(0, (start_row, start_column))]
        heapq.heapify(open_set)
        came_from = {(start_row, start_column): None}
        g_costs = {(start_row, start_column): 0}

        while open_set:
            _, current_field = heapq.heappop(open_set)
            if current_field == destination_field:
                path = []
                while current_field is not None:
                    path.insert(0, current_field)
                    current_field = came_from[current_field]
                return path

            for neighbor_field in get_neighbor_fields(*current_field):
                tentative_g_score = g_costs[current_field] + 1
                if neighbor_field not in g_costs or tentative_g_score < g_costs[neighbor_field]:
                    g_costs[neighbor_field] = tentative_g_score
                    f_score = tentative_g_score + manhattan_distance(neighbor_field, destination_field)
                    heapq.heappush(open_set, (f_score, neighbor_field))
                    came_from[neighbor_field] = current_field
        return None

    def get_mini_map_circle(self, radius):
        map_fragment = self.get_mini_map(radius)
        if map_fragment is None:
            return None

        circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        circle_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(circle_surface, (255, 255, 255, 255), (radius, radius), radius)

        map_fragment.set_colorkey((0, 0, 0))
        circle_surface.blit(map_fragment, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        return circle_surface

    def get_mini_map(self, radius):
        screen_x, screen_y = self.convert_map_position_to_screen_position(0, 0)
        if screen_x < 0:
            crop_x = abs(screen_x)
        else:
            crop_x = 0

        if screen_y < 0:
            crop_y = abs(screen_y)
        else:
            crop_y = 0

        if screen_x > 0:
            display_x = screen_x
        else:
            display_x = 0

        if screen_y > 0:
            display_y = screen_y
        else:
            display_y = 0

        screen_width, screen_height = self.game_surface.get_size()
        map_width, map_height = self._map_image.get_size()
        fragment_width = min(screen_width - display_x, map_width - crop_x)
        fragment_height = min(screen_height - display_y, map_height - crop_y)
        if fragment_width < 0 or fragment_height < 0:
            return
        map_fragment = self._map_image.subsurface((crop_x, crop_y, fragment_width, fragment_height))
        map_fragment = pygame.transform.scale(map_fragment, (radius * 2, radius * 2))

        return map_fragment

    def draw_map(self) -> None:
        screen_x, screen_y = self.convert_map_position_to_screen_position(0, 0)
        if screen_x < 0:
            crop_x = abs(screen_x)
        else:
            crop_x = 0

        if screen_y < 0:
            crop_y = abs(screen_y)
        else:
            crop_y = 0

        if screen_x > 0:
            display_x = screen_x
        else:
            display_x = 0

        if screen_y > 0:
            display_y = screen_y
        else:
            display_y = 0

        screen_width, screen_height = self.game_surface.get_size()
        map_width, map_height = self._map_image.get_size()
        fragment_width = min(screen_width - display_x, map_width - crop_x)
        fragment_height = min(screen_height - display_y, map_height - crop_y)
        if fragment_width < 0 or fragment_height < 0:
            return
        map_fragment = self._map_image.subsurface((crop_x, crop_y, fragment_width, fragment_height))
        self.game_surface.blit(map_fragment, (display_x, display_y))

        if self.game_context.is_in_debug_mode:
            self.draw_grid()

    def draw_grid(self):
        for row_nr in range(len(self._collisions_grid)):
            for column_nr in range(len(self._collisions_grid[row_nr])):
                x = column_nr * MAP_COLLISION_TILE
                y = row_nr * MAP_COLLISION_TILE
                screen_x, screen_y = self.convert_map_position_to_screen_position(x, y)
                if self._collisions_grid[row_nr][column_nr]:
                    color = RED
                    frame_width = 5
                else:
                    color = WHITE
                    frame_width = 1
                pygame.draw.rect(
                    self.game_surface,
                    color,
                    (
                        screen_x,
                        screen_y,
                        MAP_COLLISION_TILE,
                        MAP_COLLISION_TILE
                    ),
                    width=frame_width
                )
                row_nr_text = FONT_MONOSPACE_COURIER_16.render(f'{row_nr}', False, WHITE)
                column_nr_text = FONT_MONOSPACE_COURIER_16.render(f'{column_nr}', False, WHITE)
                self.game_surface.blit(row_nr_text, (screen_x, screen_y))
                self.game_surface.blit(column_nr_text, (screen_x, screen_y + row_nr_text.get_height()))

    def _draw_loading_screen(self) -> None:
        pass

    @property
    def night_overlay_alpha(self):
        if self.datetime_manager.is_first_half_of_night:
            return 0 + normalize_value(
                value=self.datetime_manager.second,
                min_val=self.datetime_manager.NIGHT_START_TIME_IN_SECONDS,
                max_val=self.datetime_manager.SECONDS_PER_DAY - 1,
                new_min=self.NIGHT_OVERLAY_ALPHA_MIN,
                new_max=self.NIGHT_OVERLAY_ALPHA_MAX
            )
        elif self.datetime_manager.is_second_half_of_night:
            return self.NIGHT_OVERLAY_ALPHA_MAX - normalize_value(
                value=self.datetime_manager.second,
                min_val=0,
                max_val=self.datetime_manager.DAY_START_TIME_IN_SECONDS - 1,
                new_min=self.NIGHT_OVERLAY_ALPHA_MIN,
                new_max=self.NIGHT_OVERLAY_ALPHA_MAX
            )

    def draw_night_overlay(self) -> None:
        if not self.datetime_manager.is_day_now:
            alpha = int(self.night_overlay_alpha)
            self.game_surface.blit(self.night_overlays[int(alpha * self.NIGHT_OVERLAY_ACCURACY)], (0, 0))
