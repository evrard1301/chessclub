from view.menu import Menu, MenuBuilder


class ConsoleMenu(Menu):
    def __init__(self, title):
        super().__init__(title)
        self.title = title

    def show(self):
        print('--------' + self.title + '--------')

        for value, menu in self.menus.items():
            print(f'\t{value}) {menu.title}')

        for entry in self.entries.values():
            print(f'\t{entry.action}) {entry.label}')


class ConsoleMenuBuilder(MenuBuilder):
    def begin_menu(self, title, action=''):
        self.menus.append(ConsoleMenu(title))
        self.actions.append(action)
        return self
