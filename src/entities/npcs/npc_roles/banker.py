from src.entities.npcs.npc_roles.npc_role import NpcRole
from src.enums.npc_role_type import NpcRoleType
from src.managers.gameplay.bank_manager import BankManager


class BankerNpc(NpcRole):
    bank_manager = None

    def __init__(self, owner_reference):
        super().__init__(owner_reference)

    def get_role_name(self):
        return NpcRoleType.BANKER

    @classmethod
    def set_managers(cls):
        cls.bank_manager = BankManager.get_instance()

    def interact(self):
        pass
