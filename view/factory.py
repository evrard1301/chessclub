from .builder import ConsoleMenuBuilder
from bs4 import BeautifulSoup


class XMLFactory:
    def __init__(self, user_input):
        self._user_input = user_input

    def load_from_file(self, filename):
        data = ''
        with open(filename) as file:
            data = file.read()

        parser = BeautifulSoup(data, 'xml')
        builder = ConsoleMenuBuilder(self._user_input)

        def parse_menu(builder, menu):
            if menu.name == 'menu':
                action = ''
                if 'action' in menu.attrs.keys():
                    action = menu['action']
                builder.begin_menu(menu['title'], action)
                for child in menu.children:
                    parse_menu(builder, child)
                builder.end()
            if menu.name == 'entry':
                builder.entry(menu.text.strip(), menu['action'])
            if menu.name == 'link':
                builder.link(menu.text.strip(), menu['action'])
            if menu.name == 'ask':
                default = None
                if 'default' in menu.attrs.keys():
                    default = menu['default']
                builder.ask(menu['action'],
                            menu.text.strip(),
                            default)

        parse_menu(builder, parser.menu)

        return builder.build()
