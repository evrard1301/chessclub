from abc import ABC
from abc import abstractmethod
from view.menu import StopAndSave


class UserInteractor(ABC):
    @abstractmethod
    def ask(self, msg):
        pass

    @abstractmethod
    def tell(self, msg):
        pass


class ConsoleUserInteractor(UserInteractor):
    def ask(self, msg):
        if msg == '\\quitter':
            raise StopAndSave()
        return input(msg)

    def tell(self, msg):
        print(msg)
