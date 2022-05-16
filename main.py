from controller.approuter import AppRouter
from controller.approuter import PrintErrorManager
from controller.controllers import MainController
from datetime import date
from model.chessclub import ChessClub
from model.datastore import TinyDBStore
from model.player import Player
from model.round import Round
from view.factory import XMLFactory
from view.userinteractor import ConsoleUserInteractor


def example_tournament(model, datastore):

    tournament = model.new_tournament('THE tournament',
                                      'ChessClub building',
                                      date(2020, 3, 7),
                                      'blitz',
                                      'my first tournament')
    tournament.add_round(Round('Round 1',
                               date(2020, 3, 8),
                               date(2020, 3, 9)))
    tournament.add_round(Round('Round 2',
                               date(2020, 3, 9),
                               date(2020, 3, 10)))
    tournament.add_round(Round('Round 3',
                               date(2020, 3, 10),
                               date(2020, 3, 11)))

    tournament.add_player(Player('Kazparov', 'Garry', '12/08/1995', 'M', '1'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Carlsen', 'Magnus', '12/08/1995', 'M', '2'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Fischer', 'Bobby', '12/08/1995', 'M', '3'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Capablanca',
                                 'Jose Raul', '12/08/1995', 'M', '4'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Karpov', 'Anatoly', '12/08/1995', 'M', '5'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Botvinnik',
                                 'Mikhail', '12/08/1995', 'M', '6'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Kramnik',
                                 'Vladimir', '12/08/1995', 'M', '7'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Lasker', 'Emanuel', '12/08/1995', 'M', '8'))
    datastore.store_player(tournament._players[-1])


if __name__ == '__main__':
    user_interactor = ConsoleUserInteractor()
    factory = XMLFactory(user_interactor)
    view = factory.load_from_file('data/menu.xml')
    datastore = TinyDBStore()
    model = ChessClub(datastore)
    # Uncomment for manual testing
    # example_tournament(model, datastore)
    router = AppRouter(user_interactor, model, view)
    router.set_error_manager(PrintErrorManager(user_interactor))
    router.set_controller(MainController())

    try:
        router.run()
    except KeyboardInterrupt:
        print()
        model.quit()
