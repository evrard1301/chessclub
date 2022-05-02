from .console import ConsoleMenu
from .console import ConsoleMenuInput
from .menu import Menu
from .menu import MenuInput


class MenuBuilder:
    def __init__(self, user_input):
        self._user_input = user_input
        self._menus = []

    def build(self):
        menu = self._menus[-1][1]
        self._menus.pop()
        return menu

    def begin_menu(self, title, action):
        self._menus.append((action, Menu(title)))
        return self

    def end(self):
        if len(self._menus) > 1:
            action, menu = self._menus.pop()
            self._menus[-1][1].add(menu, action)
        return self

    def entry(self, title, action):
        """Menu entry is not a submenu."""
        self._menus[-1][1].add(title, action)
        return self

    def ask(self, action, text, default):
        self._menus[-1][1].add_input(action,
                                     MenuInput(self._user_input,
                                               text,
                                               default))
        return self

    def link(self, menu_title, action):
        """Link to another menu."""
        menu = None
        for entry in self._menus:
            if entry[1].title == menu_title:
                menu = entry[1]
                break
        self._menus[-1][1].add(menu, action)
        return self


class ConsoleMenuBuilder(MenuBuilder):
    def __init__(self, user_input):
        super().__init__(user_input)

    def begin_menu(self, title, action):
        self._menus.append((action, ConsoleMenu(title)))
        return self

    def ask(self, action, text, default):
        self._menus[-1][1].add_input(action,
                                     ConsoleMenuInput(self._user_input,
                                                      text,
                                                      default))
        return self
