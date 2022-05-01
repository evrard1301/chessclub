from view.factory import XMLFactory
from model.chessclub import ChessClub
from model.datastore import DataStore
from controller.approuter import AppRouter
from controller.controllers import MainController

if __name__ == '__main__':
    factory = XMLFactory()
    view = factory.load_from_file('data/menu.xml')
    datastore = DataStore()
    model = ChessClub(datastore)
    router = AppRouter(model, view)
    router.set_controller(MainController())
    router.run()
