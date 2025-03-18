from abc import abstractmethod


class Attack:
    def __init__(self, attacker_reference):
        self.attacker = attacker_reference

    @abstractmethod
    def perform(self):
        pass
