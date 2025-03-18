import os

from src.enums.chat_message_color_type import ChatMessageColorType
from src.paths import DIR_ASSETS_SOUNDTRACKS, FILE_SOUNDTRACK_DAY, \
    FILE_SOUNDTRACK_NIGHT


class DatetimeManager:
    _instance = None

    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3_600
    HOURS_PER_DAY = 24
    SECONDS_PER_DAY = HOURS_PER_DAY * SECONDS_PER_HOUR
    DAYS_PER_WEEK = 7
    MONTHS_PER_YEAR = 12

    TIME_SCALE = SECONDS_PER_MINUTE

    DAY_START_MESSAGE = 'The new day has dawned!'
    DAY_START_HOUR = 7
    DAY_START_TIME_IN_SECONDS = DAY_START_HOUR * SECONDS_PER_HOUR

    NIGHT_START_MESSAGE = 'The night has come!'
    NIGHT_START_HOUR = 19
    NIGHT_START_TIME_IN_SECONDS = NIGHT_START_HOUR * SECONDS_PER_HOUR

    WEEKDAY_NAMES = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

    MONTH_NAMES = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    MONTH_LENGTHS = {
        'January': 31,
        'February': 28,
        'March': 31,
        'April': 30,
        'May': 31,
        'June': 30,
        'July': 31,
        'August': 31,
        'September': 30,
        'October': 31,
        'November': 30,
        'December': 31
    }

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

            self.map_manager = None
            self.sound_manager = None
            self.chat_manager = None

            self.second = 19 * self.SECONDS_PER_HOUR
            self.float_seconds: float = 0

            self._weekday = 0
            self._monthday = 0
            self._month = 0

            self.was_day_previously = self.is_day_now

    def setup_references(self):
        from src.managers.ui.chat_manager import ChatManager
        from src.managers.gameplay.map_manager import MapManager
        from src.managers.core.sound_manager import SoundManager

        self.map_manager = MapManager.get_instance()
        self.sound_manager = SoundManager.get_instance()
        self.chat_manager = ChatManager.get_instance()

    def get_formatted_time(self, seconds):
        hours = int(seconds // self.SECONDS_PER_HOUR)
        minutes = int((seconds % self.SECONDS_PER_HOUR) // self.SECONDS_PER_MINUTE)
        seconds = int(seconds % self.SECONDS_PER_HOUR % self.SECONDS_PER_MINUTE)
        return f'{hours}h {minutes}min {seconds}s'

    @property
    def formatted_datetime(self) -> str:
        return f'{self.weekday}, {self.monthday} of {self.month} {self.hour:02}:{self.minute:02}'

    @property
    def hour(self) -> int:
        return int(self.second // self.SECONDS_PER_HOUR)

    @property
    def minute(self) -> int:
        return int((self.second % self.SECONDS_PER_HOUR) // self.SECONDS_PER_MINUTE)

    @property
    def weekday(self) -> str:
        return self.WEEKDAY_NAMES[self._weekday]

    @property
    def month(self) -> str:
        return self.MONTH_NAMES[self._month]

    @property
    def monthday(self) -> str:
        return f'{self._monthday + 1}{self.monthday_suffix}'

    @property
    def monthday_suffix(self):
        if (self._monthday + 1) in [1, 2, 3, 21, 22, 23, 31]:
            unit = (self._monthday + 1) % 10
            if unit == 1:
                return 'st'
            elif unit == 2:
                return 'nd'
            elif unit == 3:
                return 'rd'
        else:
            return 'th'

    @property
    def is_day_now(self) -> bool:
        return self.DAY_START_HOUR <= self.hour < self.NIGHT_START_HOUR

    def switch_day_night_soundtrack(self) -> None:
        if self.is_day_now:
            soundtrack_path = os.path.join(
                DIR_ASSETS_SOUNDTRACKS,
                f'map{self.map_manager.map_id}',
                FILE_SOUNDTRACK_DAY
            )
        else:
            soundtrack_path = os.path.join(
                DIR_ASSETS_SOUNDTRACKS,
                f'map{self.map_manager.map_id}',
                FILE_SOUNDTRACK_NIGHT
            )
        self.sound_manager.play_soundtrack(soundtrack_path)

    def increment_time(self, delta_time: float) -> None:
        self.float_seconds += self.TIME_SCALE * delta_time
        if self.float_seconds >= 1.0:
            seconds_to_add = int(self.float_seconds)
            self.float_seconds -= seconds_to_add
            self.second += seconds_to_add

            if self.second >= (self.SECONDS_PER_HOUR * self.HOURS_PER_DAY):
                self._weekday += 1
                self._monthday += 1
                if self._monthday >= self.MONTH_LENGTHS.get(self.MONTH_NAMES[self._month]):
                    self._month += 1
                    self._monthday = 0
                    if self._month >= self.MONTHS_PER_YEAR:
                        self._month = 0
                if self._weekday >= self.DAYS_PER_WEEK:
                    self._weekday = 0
                self.second = 0

            if self.is_day_now:
                if not self.was_day_previously:
                    self.was_day_previously = True
                    self.switch_day_night_soundtrack()
                    self.chat_manager.push_message_to_chat(self.DAY_START_MESSAGE, ChatMessageColorType.SYSTEM)
            elif self.was_day_previously:
                self.was_day_previously = False
                self.switch_day_night_soundtrack()
                self.chat_manager.push_message_to_chat(self.NIGHT_START_MESSAGE, ChatMessageColorType.SYSTEM)

    @property
    def is_first_half_of_night(self) -> bool:
        return self.second >= self.NIGHT_START_TIME_IN_SECONDS

    @property
    def is_second_half_of_night(self):
        return self.second < self.DAY_START_TIME_IN_SECONDS
