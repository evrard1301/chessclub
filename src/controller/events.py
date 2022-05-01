from abc import ABC, abstractmethod


class Event:
    def __init__(self, name, **kwargs):
        self.name = name
        self.args = kwargs


class EventListener(ABC):
    @abstractmethod
    def on_event(self, event):
        pass
