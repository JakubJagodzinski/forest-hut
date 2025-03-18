from abc import abstractmethod


class Spell:
    game_clock = None
    error_messages_manager = None
    quotes_manager = None

    def __init__(self, caster_reference, cast_time_in_seconds, cooldown_time_in_seconds, spell_icon_name=None):
        self.caster_reference = caster_reference
        self.cast_time_in_seconds = cast_time_in_seconds
        self.cooldown_time_in_seconds = cooldown_time_in_seconds
        self.spell_icon_name = spell_icon_name

        self._is_being_casted = False
        self.cast_start_time = 0.0
        self.cast_end_time = float('-inf')

    @classmethod
    def setup_references(cls):
        from src.managers.ui.error_messages_manager import ErrorMessagesManager
        from src.managers.gameplay.quotes_manager import QuotesManager
        from src.game_clock import GameClock

        cls.game_clock = GameClock.get_instance()
        cls.error_messages_manager = ErrorMessagesManager.get_instance()
        cls.quotes_manager = QuotesManager.get_instance()

    def get_cast_time(self) -> float:
        return self.cast_time_in_seconds

    def get_remaining_cast_time(self) -> float:
        return self.cast_time_in_seconds - (self.game_clock.game_time - self.cast_start_time)

    def is_ready(self) -> bool:
        return (self.game_clock.game_time - self.cast_end_time) > self.cooldown_time_in_seconds

    def is_being_casted(self) -> bool:
        return self._is_being_casted

    def is_cast_finished(self) -> bool:
        return (self.game_clock.game_time - self.cast_start_time) > self.cast_time_in_seconds

    def begin_cast(self) -> None:
        self._is_being_casted = True
        self.cast_start_time = self.game_clock.game_time

    def cancel_cast(self) -> None:
        self._is_being_casted = False

    def handle_casting(self) -> None:
        if self.is_being_casted and not self.is_cast_finished():
            self.during_cast_action()

    def handle_cast_finish(self) -> None:
        if self._is_being_casted and self.is_cast_finished():
            self.final_action()
            self._is_being_casted = False

    @abstractmethod
    def during_cast_action(self):
        pass

    @abstractmethod
    def final_action(self):
        pass

    @abstractmethod
    def draw_casting_animation(self):
        pass

    def draw_casting_bar(self) -> None:
        if self.is_being_casted:
            self.caster_reference.casting_bar.draw(
                int(self.get_remaining_cast_time() * 100),
                int(self.cast_time_in_seconds * 100)
            )
