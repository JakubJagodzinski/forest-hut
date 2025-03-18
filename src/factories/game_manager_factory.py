from typing import override

from src.enums.game_manager_type import GameManagerType
from src.factories.manager_factory import ManagerFactory
from src.managers.gameplay.bank_manager import BankManager
from src.managers.gameplay.combat_manager import CombatManager
from src.managers.gameplay.conversation_manager import ConversationManager
from src.managers.gameplay.datetime_manager import DatetimeManager
from src.managers.gameplay.equipment_manager import EquipmentManager
from src.managers.gameplay.interactive_objects_manager import InteractiveObjectsManager
from src.managers.gameplay.inventory_manager import InventoryManager
from src.managers.gameplay.kill_series_manager import KillSeriesManager
from src.managers.gameplay.loot_manager import LootManager
from src.managers.gameplay.map_manager import MapManager
from src.managers.gameplay.npcs_manager import NpcsManager
from src.managers.gameplay.player_manager import PlayerManager
from src.managers.gameplay.potions_manager import PotionsManager
from src.managers.gameplay.quotes_manager import QuotesManager
from src.managers.gameplay.vendor_manager import VendorManager
from src.managers.ui.chat_manager import ChatManager
from src.managers.ui.command_manager import CommandManager
from src.managers.ui.error_messages_manager import ErrorMessagesManager
from src.managers.ui.interface_manager import InterfaceManager
from src.managers.ui.item_icons_manager import ItemIconsManager
from src.managers.ui.spell_icons_manager import SpellIconsManager


class GameManagerFactory(ManagerFactory):

    def __init__(self):
        super().__init__()

    @override
    def create_managers(self):
        self.managers = {
            GameManagerType.BANK: BankManager(),
            GameManagerType.COMBAT: CombatManager(),
            GameManagerType.CONVERSATION: ConversationManager(),
            GameManagerType.DATETIME: DatetimeManager(),
            GameManagerType.EQUIPMENT: EquipmentManager(),
            GameManagerType.INTERACTIVE_OBJECTS: InteractiveObjectsManager(),
            GameManagerType.INVENTORY: InventoryManager(),
            GameManagerType.KILL_SERIES: KillSeriesManager(),
            GameManagerType.LOOT: LootManager(),
            GameManagerType.MAP: MapManager(),
            GameManagerType.NPCS: NpcsManager(),
            GameManagerType.PLAYER: PlayerManager(),
            GameManagerType.POTIONS: PotionsManager(),
            GameManagerType.QUOTES: QuotesManager(),
            GameManagerType.VENDOR: VendorManager(),
            GameManagerType.CHAT: ChatManager(),
            GameManagerType.COMMAND: CommandManager(),
            GameManagerType.ERROR_MESSAGES: ErrorMessagesManager(),
            GameManagerType.INTERFACE: InterfaceManager(),
            GameManagerType.ITEM_ICONS: ItemIconsManager(),
            GameManagerType.SPELL_ICONS: SpellIconsManager(),
        }
