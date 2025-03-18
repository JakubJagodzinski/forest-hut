from abc import ABC, abstractmethod


class NpcRole(ABC):

    def __init__(self, owner_reference):
        self.owner_reference = owner_reference

    @abstractmethod
    def get_role_name(self):
        pass

    @abstractmethod
    def interact(self):
        pass
