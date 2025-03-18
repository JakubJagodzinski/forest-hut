from abc import abstractmethod


class ManagerFactory:

    def __init__(self):
        self.managers = {}

    @abstractmethod
    def create_managers(self):
        pass

    def get_manager(self, manager_type):
        return self.managers.get(manager_type)

    def reset_managers(self):
        for key in list(self.managers.keys()):
            self.managers[key] = None

    def setup_all_references(self):
        for manager in self.managers.values():
            if hasattr(manager, 'setup_references'):
                manager.setup_references()
