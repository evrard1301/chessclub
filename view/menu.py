from abc import ABC
from abc import abstractmethod
from controller.events import Event
from controller.events import EventSource


class MenuInput(ABC):
    def __init__(self, user_input, text, default=None):
        self._user_input = user_input
        self._text = text
        self._default = default

    @abstractmethod
    def ask(self):
        pass


class Menu:
    """Composite structure representing an abstract menu."""
    def __init__(self, title):
        self._title = title
        self._inputs = {}
        self._nexts = {}

    @property
    def title(self):
        return self._title

    def add_input(self, action, menu_input):
        if action not in self._inputs.keys():
            self._inputs[action] = []
        self._inputs[action].append(menu_input)

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
        self._responses = []

    def menu(self):
        return self._menu

    def __getitem__(self, index):
        if index >= len(self._responses):
            return None

        return self._responses[index]

    def nav(self, action):
        next_menu = self._menu.get_menu_by_action(action)

        if not isinstance(next_menu, str) and next_menu.is_submenu():
            self._menu = next_menu
            self.notify(Event('goto', menu=next_menu))
        else:
            self.notify(Event('activate', action=action, entry=next_menu))

        if action in self._menu._inputs.keys():
            i = 1
            for menu_input in self._menu._inputs[action]:
                self._responses.append(menu_input.ask())
                self.notify(Event('ask',
                                  question=menu_input,
                                  response=self._responses[-1],
                                  action=action,
                                  index=i,
                                  count=len(self._menu._inputs[action])))
                i += 1


class MenuError(Exception):
    pass
