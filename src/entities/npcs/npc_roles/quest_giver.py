from src.entities.npcs.npc_roles.npc_role import NpcRole
from src.enums.npc_role_type import NpcRoleType


class QuestGiver(NpcRole):

    def __init__(self, owner_reference):
        super().__init__(owner_reference)

    def get_role_name(self):
        return NpcRoleType.QUEST_GIVER

    def interact(self):
        pass
