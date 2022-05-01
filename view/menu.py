from abc import ABC, abstractmethod
from controller.events import Event, EventSource


class Menu:
    """Composite structure representing an abstract menu."""
    def __init__(self, title):
        self._title = title
        self._nexts = {}

    @property
    def title(self):
        return self._title

    def add(self, next_menu, action):
        self._nexts[action] = next_menu

    def is_submenu(self):
        return len(self._nexts) > 0

    def get_menu_by_action(self, action):
        if action not in self._nexts.keys():
            raise MenuError(f'no menu with action "{action}"')
        return self._nexts[action]

    @abstractmethod
    def show(self):
        """Expose the menu to the user."""
        pass
    
class MenuSession(EventSource):
    """Represent a stateful menu navigation."""
    def __init__(self, menu):
        super().__init__()
        self._menu = menu

    def menu(self):
        return self._menu

    def nav(self, action):
        next_menu = self._menu.get_menu_by_action(action)
        if not isinstance(next_menu, str) and next_menu.is_submenu():
            self._menu = next_menu
            self.notify(Event('goto', menu=next_menu))
        else:
            self.notify(Event('activate', action=action, entry=next_menu))


class MenuError(Exception):
    pass
