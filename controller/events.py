from abc import ABC
from abc import abstractmethod


class Event:
    def __init__(self, name, **kwargs):
        self._name = name
        self._values = kwargs

    def name(self):
        return self._name

    def get(self, value_name):
        return self._values[value_name]


class EventSource:
    def __init__(self):
        self._listeners = []

    def add_listener(self, listener):
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def notify(self, event):
        """Notify an event to all the listeners."""
        for listener in self._listeners:
            listener.on_event(event)


class EventListener(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def on_event(self):
        """Called when the event source notify an event."""
        pass
