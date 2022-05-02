from abc import ABC
from abc import abstractmethod


class UserInput(ABC):
    @abstractmethod
    def ask(self, msg):
        pass


class ConsoleUserInput(UserInput):
    def ask(self, msg):
        return input(msg)
