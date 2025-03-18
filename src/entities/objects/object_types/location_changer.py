from typing import override

from database.game_database_table_columns_names import MapsTable
from src.entities.objects.object import Object


class LocationChanger(Object):

    def __init__(self, game_surface, map_id, x, y, destination_map_id, destination_x, destination_y,
                 draw_size, name, sprite_name):
        if name is None:
            from src.database_service import DatabaseService
            name = DatabaseService.get_map_info(destination_map_id)[MapsTable.MAP_NAME]

        super().__init__(game_surface, map_id, x, y, draw_size, name, sprite_name)

        self.destination_map_id = destination_map_id
        self.destination_x = destination_x
        self.destination_y = destination_y

    @override
    def interact(self):
        self.map_manager.load_map(self.destination_map_id)
        self.player_manager.set_position(self.destination_x, self.destination_y)
        self.player_manager.set_map_id(self.destination_map_id)
        self.map_manager.load_map(self.destination_map_id)
        self.loot_manager.update()
        self.interactive_objects_manager.update()
        self.npcs_manager.update()
        self.quotes_manager.clear_quotes_queue()
