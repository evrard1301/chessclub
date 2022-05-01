from controller import ViewInteractor, Event


class MenuError(Exception):
    pass


class MenuEntry:
    action = ''
    label = ''

    def callback():
        pass


class MenuSession:
    def __init__(self, menu):
        self.menu = menu

    def goto(self, action):
        if action in self.menu.entries.keys():
            self.menu.entries[action].callback()
            self.menu.notify(Event('goto_entry', entry=self.menu.entries[action]))
            return

        if action in self.menu.menus.keys():
            self.menu = self.menu.menus[action]
            self.menu.notify(Event('goto_menu', menu=self.menu))
            return

        raise MenuError(
            f'"{action}" is not'
            f' defined for menu {self.menu.title}')

    def show(self):
        self.menu.show()


class Menu(ViewInteractor):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.entries = {}
        self.menus = {}

    def add_entry(self, action, label, callback=lambda: True):
        e = MenuEntry()
        e.action = action
        e.label = label
        e.callback = callback
        self.entries[action] = e
        return e

    def add_menu(self, action, menu):
        self.menus[action] = menu

    def session(self):
        return MenuSession(self)

    def show(self):
        pass


class MenuBuilder:
    def __init__(self):
        self.menus = []
        self.actions = []
        
    def build(self):
        return self.menus[-1]

    def entry(self, action, label):
        self.menus[-1].add_entry(action, label)
        return self

    def menu(self, action, menu_title):
        for menu in self.menus:
            if menu.title == menu_title:
                self.menus[-1].add_menu(action, menu)
                return self
        return self

    def begin_menu(self, title, action=''):
        self.menus.append(Menu(title))
        self.actions.append(action)
        return self

    def end_menu(self):
        if len(self.menus) > 1:
            action = self.actions.pop()
            menu = self.menus.pop()
            self.menus[-1].add_menu(action, menu)
        return self
