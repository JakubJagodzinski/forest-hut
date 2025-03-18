class ErrorMessagesRenderer:

    def __init__(self, game_screen):
        self.game_screen = game_screen
        self.error_messages_manager = None

    def setup_references(self):
        from src.managers.ui.error_messages_manager import ErrorMessagesManager
        self.error_messages_manager = ErrorMessagesManager.get_instance()

    def draw(self):
        pass