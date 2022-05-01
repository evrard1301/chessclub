from abc import ABC, abstractmethod


class UserInput(ABC):
    @abstractmethod
    def ask(self, msg):
        pass


class ConsoleUserInput(UserInput):
    def ask(self, msg):
        return input(msg)
