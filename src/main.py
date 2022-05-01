"""Main project file."""
from controller import AppFactory

if __name__ == '__main__':
    factory = AppFactory()
    app = factory.make_from_file('../data/menu.xml')
    app.run()
