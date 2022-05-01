from bs4 import BeautifulSoup
from . import AppController, MainController
from model import ChessClub
from view import ConsoleMenuBuilder


class AppFactory:
    def __init__(self):
        pass

    def _make_view(self, filename):
        xml_str = ''
        with open(filename) as file:
            xml_str = file.read()

        parser = BeautifulSoup(xml_str, 'xml')
        builder = ConsoleMenuBuilder()

        def parse_menu(builder, element):
            if element.name == 'menu':
                if 'action' in element.attrs.keys():
                    builder.begin_menu(element['title'],
                                       action=element['action'])
                else:
                    builder.begin_menu(element['title'])

                for child in element.children:
                    parse_menu(builder, child)

                builder.end_menu()
            elif element.name == 'entry':
                builder.entry(element['action'], element.text)
            elif element.name == 'menu-entry':
                builder.menu(element['action'], element['title'])
        parse_menu(builder, parser.menu)
        return builder.build()

    def make_from_file(self, filename):
        app = AppController()
        model = ChessClub()
        view = self._make_view(filename)

        app.add_controller('main', MainController(model, view))
        return app
