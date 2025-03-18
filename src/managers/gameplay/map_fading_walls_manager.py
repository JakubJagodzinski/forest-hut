import pygame

from database.game_database_table_columns_names import MapFadingWallPositionsTable, MapFadingWallsTable
from src.database_service import DatabaseService


class MapFadingWall:

    def __init__(self, map_id, x, y, width, height, image_path):
        self.map_id = map_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fade_rect = pygame.Rect(
            x,
            y,
            width,
            height
        )
        self.alpha = 255
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def is_colliding(self, position):
        return self.fade_rect.collidepoint(position)


class MapFadingWallsManager:

    def __init__(self):
        self.map_manager = None
        self.map_fading_walls = {}

    def setup_references(self):
        from src.managers.gameplay.map_manager import MapManager

        self.map_manager = MapManager.get_instance()

    def load_map_fading_walls(self):
        current_map_id = self.map_manager.map_id
        if current_map_id not in self.map_fading_walls:
            self.map_fading_walls[current_map_id] = {}

            map_fading_wall_positions = DatabaseService.get_map_fading_wall_positions(current_map_id)
            map_fading_wall_ids = {
                map_fading_wall_id
                for map_fading_wall_id in map_fading_wall_positions[MapFadingWallPositionsTable.FADING_WALL_ID]
            }
            map_fading_walls = DatabaseService.get_map_fading_walls(map_fading_wall_ids)

            for map_fading_wall_position in map_fading_wall_positions:
                map_fading_wall = map_fading_walls[MapFadingWallsTable.FADING_WALL_ID]
                self.map_fading_walls[map_fading_wall.id] = MapFadingWall(
                    map_id=map_fading_wall_position[MapFadingWallPositionsTable.MAP_ID],
                    x=map_fading_wall_position[MapFadingWallPositionsTable.X],
                    y=map_fading_wall_position[MapFadingWallPositionsTable.Y],
                    width=map_fading_wall[MapFadingWallsTable.WALL_WIDTH],
                    height=map_fading_wall[MapFadingWallsTable.WALL_HEIGHT],
                    image_path=map_fading_wall[MapFadingWallsTable.IMAGE_PATH]
                )
