from typing import override

from src.entities.npcs.npc_roles.npc_role import NpcRole
from src.enums.npc_role_type import NpcRoleType
from src.database_service import DatabaseService


class Vendor(NpcRole):
    vendor_manager = None
    loot_manager = None

    def __init__(self, owner_reference):
        super().__init__(owner_reference)
        self.items = self.generate_items()

    def get_role_name(self):
        return NpcRoleType.VENDOR

    @classmethod
    def setup_references(cls):
        from src.managers.gameplay.loot_manager import LootManager
        from src.managers.gameplay.vendor_manager import VendorManager

        cls.vendor_manager = VendorManager.get_instance()
        cls.loot_manager = LootManager.get_instance()

    def get_items(self):
        return self.items

    def generate_items(self):
        items_to_generate = self.vendor_manager.grid_size
        generated_items = DatabaseService.get_random_items(items_to_generate)
        return [[generated_item, 1] for generated_item in generated_items]

    @override
    def interact(self):
        self.vendor_manager.open(self, self.owner_reference)
