from src.common_utils import quit_game
from src.enums.chat_message_color_type import ChatMessageColorType
from src.enums.command_type import CommandType


class Command:

    def __init__(self, action, args=None, kwargs=None):
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        arguments = []

        if self.args is not None:
            arguments.append(self.args)
        if self.kwargs is not None:
            arguments.append(self.kwargs)
        if len(arguments) > 0:
            self.action(*arguments)
        else:
            self.action()


class CommandManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

            self.chat_manager = None
            self.player_manager = None
            self.map_manager = None
            self.datetime_manager = None
            self.game_clock = None

            self.commands = {}

    def setup_references(self):
        from src.managers.ui.chat_manager import ChatManager
        from src.managers.gameplay.datetime_manager import DatetimeManager
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.gameplay.player_manager import PlayerManager
        from src.game_clock import GameClock

        self.game_clock = GameClock.get_instance()
        self.chat_manager = ChatManager.get_instance()
        self.player_manager = PlayerManager.get_instance()
        self.map_manager = MapManager.get_instance()
        self.datetime_manager = DatetimeManager.get_instance()

    def set_commands(self):
        self.add_command(CommandType.QUIT, quit_game)
        self.add_command(CommandType.GAME_TIME, self.send_game_time_message)
        self.add_command(CommandType.POSITION, self.send_player_position_message)

    def add_command(self, command_name: str, action: callable, args=None, kwargs=None) -> None:
        self.commands[command_name] = Command(action, args, kwargs)

    def get_command_by_name(self, command_name: str) -> Command | None:
        if command_name in self.commands:
            return self.commands[command_name]
        else:
            return None

    def use_command(self, command_name: str) -> bool:
        command = self.get_command_by_name(command_name)
        if command is None:
            return False
        else:
            command.execute()
            return True

    def send_game_time_message(self):
        self.chat_manager.push_message_to_chat(
            f'Game time: {self.datetime_manager.get_formatted_time(self.game_clock.game_time)}',
            ChatMessageColorType.SYSTEM
        )

    def send_player_position_message(self):
        x = int(self.player_manager.x)
        y = int(self.player_manager.y)
        row = int(self.player_manager.row)
        column = int(self.player_manager.column)
        self.chat_manager.push_message_to_chat(
            f'''{self.map_manager.get_location_name_with_levels()}\n
                    x: {x} y: {y} (row: {row}, column: {column})
                    ''',
            ChatMessageColorType.SYSTEM
        )
