from .menu import Menu


class ConsoleMenu(Menu):
    def __init__(self, title):
        super().__init__(title)

    def show(self):
        self._show_menu(self)

    def _show_menu(self, menu):
        print(menu.title)
        for action, value in menu._nexts.items():
            if not isinstance(value, str):
                print(' ', '[' + action + ']', value.title)
            else:
                print(' ', '[' + action + ']', value)
