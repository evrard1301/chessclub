from view.factory import XMLFactory
from view.userinput import ConsoleUserInput
from model.chessclub import ChessClub
from model.datastore import DataStore
from controller.approuter import AppRouter
from controller.controllers import MainController

if __name__ == '__main__':
    user_input = ConsoleUserInput()
    factory = XMLFactory(user_input)
    view = factory.load_from_file('data/menu.xml')
    datastore = DataStore()
    model = ChessClub(datastore)
    router = AppRouter(user_input, model, view)
    router.set_controller(MainController())
    router.run()
