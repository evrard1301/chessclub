from abc import ABC
from abc import abstractmethod


class UserInteractor(ABC):
    @abstractmethod
    def ask(self, msg):
        pass

    @abstractmethod
    def tell(self, msg):
        pass


class ConsoleUserInteractor(UserInteractor):
    def ask(self, msg):
        return input(msg)

    def tell(self, msg):
        print(msg)
