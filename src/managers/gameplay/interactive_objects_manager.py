from database.game_database_table_columns_names import MapObjectPositionsTable, ObjectsTable, ObjectTypesTable, \
    LocationChangersTable
from src.entities.character import CHARACTER_DRAW_SIZE
from src.entities.objects.object_types.location_changer import LocationChanger
from src.enums.interactive_object_type import InteractiveObjectType
from src.database_service import DatabaseService


class InteractiveObjectsManager:
    _instance = None

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
            self.current_map_id = None

            self.interactive_objects = {}

    def setup_references(self):
        from src.managers.gameplay.map_manager import MapManager

        self.map_manager = MapManager.get_instance()

    def update(self):
        self.load_interactive_objects()

    def load_interactive_objects(self):
        self.current_map_id = self.map_manager.map_id
        if self.current_map_id not in self.interactive_objects:
            self.interactive_objects[self.current_map_id] = []
            objects_on_map = DatabaseService.get_objects_on_map(self.current_map_id)
            object_on_map_ids = {object_on_map[MapObjectPositionsTable.OBJECT_ID] for object_on_map in objects_on_map}
            loaded_objects = DatabaseService.get_objects_by_ids(object_on_map_ids)
            object_types = DatabaseService.get_object_types()
            for object_on_map in objects_on_map:
                object_id = object_on_map[MapObjectPositionsTable.OBJECT_ID]
                object_type = object_types[object_id]
                object_type_name = object_type[ObjectTypesTable.OBJECT_TYPE_NAME]
                object_type_data = DatabaseService.get_object_type_data(
                    object_type[ObjectTypesTable.OBJECT_TYPE_TABLE_NAME],
                    object_id
                )
                object_name = loaded_objects[object_id][ObjectsTable.OBJECT_NAME]
                sprite_name = loaded_objects[object_id][ObjectsTable.SPRITE_NAME]
                if object_type_name == InteractiveObjectType.LOCATION_CHANGER:
                    self.interactive_objects[self.current_map_id].append(
                        LocationChanger(
                            game_surface=self.game_surface,
                            map_id=self.current_map_id,
                            x=object_on_map[MapObjectPositionsTable.X],
                            y=object_on_map[MapObjectPositionsTable.Y],
                            destination_map_id=object_type_data[LocationChangersTable.DESTINATION_MAP_ID],
                            destination_x=object_type_data[LocationChangersTable.DESTINATION_X],
                            destination_y=object_type_data[LocationChangersTable.DESTINATION_Y],
                            draw_size=CHARACTER_DRAW_SIZE,
                            name=object_name,
                            sprite_name=sprite_name
                        )
                    )

    def draw_interactive_objects(self):
        for interactive_object in self.interactive_objects[self.map_manager.map_id]:
            interactive_object.draw()
