from typing import override

from src.enums.global_manager_type import GlobalManagerType
from src.factories.manager_factory import ManagerFactory
from src.managers.core.accounts_manager import AccountsManager
from src.managers.core.mouse_manager import MouseManager
from src.managers.core.sound_manager import SoundManager


class GlobalManagerFactory(ManagerFactory):

    def __init__(self):
        super().__init__()

    @override
    def create_managers(self):
        self.managers = {
            GlobalManagerType.SOUND: SoundManager(),
            GlobalManagerType.ACCOUNTS: AccountsManager(),
            GlobalManagerType.MOUSE: MouseManager()
        }
