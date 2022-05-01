from view.factory import XMLFactory
from view.menu import MenuSession

if __name__ == '__main__':
    factory = XMLFactory()
    menu = factory.load_from_file('data/menu.xml')
    session = MenuSession(menu)

    while True:
        session.menu().show()
        x = input('> ')
        session.nav(x)
