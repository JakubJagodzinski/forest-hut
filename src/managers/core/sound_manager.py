import pygame

from src.paths import PATH_LOGIN_SCREEN_SOUNDTRACK


class SoundManager:
    _instance = None

    _sounds = {}

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
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            # pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.set_volume(0)
            self.sounds = {}

    @staticmethod
    def play_login_screen_soundtrack():
        SoundManager.play_soundtrack(PATH_LOGIN_SCREEN_SOUNDTRACK)

    @staticmethod
    def switch_soundtrack_pause():
        if pygame.mixer.music.get_busy:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    @staticmethod
    def play_soundtrack(soundtrack_path):
        try:
            pygame.mixer.music.load(soundtrack_path)
            pygame.mixer.music.play(-1)
        except:
            pygame.mixer.music.load(PATH_LOGIN_SCREEN_SOUNDTRACK)
            pygame.mixer.music.play(-1)

    def load_sounds(self):
        pass

    @classmethod
    def play_sound(cls, sound_name):
        if sound_name in cls._sounds:
            cls._sounds[sound_name].play()
