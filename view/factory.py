from bs4 import BeautifulSoup
from .builder import ConsoleMenuBuilder

class XMLFactory:
    def __init__(self):
        pass

    def load_from_file(self, filename):
        data = ''
        with open(filename) as file:
            data = file.read()

        parser = BeautifulSoup(data, 'xml')
        builder = ConsoleMenuBuilder()

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
                builder.entry(menu.text, menu['action'])
            if menu.name == 'link':
                builder.link(menu.text, menu['action'])
        
        parse_menu(builder, parser.menu)

        return builder.build()
