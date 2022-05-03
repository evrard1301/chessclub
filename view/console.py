from .menu import Menu
from .menu import MenuInput


class ConsoleMenuInput(MenuInput):
    def __init__(self, user_interactor, text, default=None):
        super().__init__(user_interactor, text, default)

    def ask(self):
        if self._default is None:
            default = ''
        else:
            default = f'({self._default})'
        res = self._user_interactor.ask(self._text + default + ': ')
        if res.strip() == '':
            return default[1:-1]
        return res


class ConsoleMenu(Menu):
    def __init__(self, title, user_interactor):
        super().__init__(title, user_interactor)

    def show(self):
        self._show_menu(self)

    def _show_menu(self, menu):
        print(menu.title)
        for action, value in menu._nexts.items():
            if not isinstance(value, str):
                print(' ', '[' + action + ']', value.title)
            else:
                print(' ', '[' + action + ']', value)
