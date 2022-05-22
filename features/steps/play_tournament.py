from behave import given, when, then
from model.chessclub import ChessClub
from model.datastore import InMemoryStore
from model.player import Player
from model.round import Round
from datetime import date
from view.factory import XMLFactory
from view.userinteractor import UserInteractor
from controller.approuter import AppRouter
from controller.controllers import MainController


class MyUserInteractor(UserInteractor):
    def __init__(self):
        self._responses = []
        self.history = []
        self._told = []

    def ask(self, msg):
        if len(self._responses) == 0:
            m = msg
            if len(self._told) > 0:
                m = self._told[-1]
            raise Exception(f'no answer for {m}')
        r = self._responses[0]
        print(r)
        del self._responses[0]
        return r

    def tell(self, msg):
        print('-> ', msg)
        self._told.append(msg)

    def add_response(self, response):
        self._responses.append(response)
        self.history.append(response)


@given('a tournament')
def step_impl(ctx):
    ctx.first_run = True
    user_interactor = MyUserInteractor()
    ctx.io = user_interactor
    data_store = InMemoryStore()
    ctx.data = data_store
    model = ChessClub(data_store)
    factory = XMLFactory(user_interactor)
    view = factory.load_from_file('data/menu.xml')
    router = AppRouter(user_interactor, model, view)
    ctx.router = router
    router.set_controller(MainController())
    ctx.starts = []
    ctx.ends = []

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
    data_store.store_player(tournament._players[-1])
    tournament.add_player(Player('Carlsen', 'Magnus', '12/08/1995', 'M', '2'))
    data_store.store_player(tournament._players[-1])
    tournament.add_player(Player('Fischer', 'Bobby', '12/08/1995', 'M', '3'))
    data_store.store_player(tournament._players[-1])
    tournament.add_player(Player('Capablanca',
                                 'Jose Raul', '12/08/1995', 'M', '4'))
    data_store.store_player(tournament._players[-1])
    tournament.add_player(Player('Karpov', 'Anatoly', '12/08/1995', 'M', '5'))
    data_store.store_player(tournament._players[-1])
    tournament.add_player(Player('Botvinnik',
                                 'Mikhail', '12/08/1995', 'M', '6'))
    data_store.store_player(tournament._players[-1])
    tournament.add_player(Player('Kramnik',
                                 'Vladimir', '12/08/1995', 'M', '7'))
    data_store.store_player(tournament._players[-1])
    tournament.add_player(Player('Lasker', 'Emanuel', '12/08/1995', 'M', '8'))
    data_store.store_player(tournament._players[-1])
    ctx.tournament = tournament

    @then('player {name} score is {score}')
    def step_impl(ctx, name, score):
        if ctx.first_run:
            ctx.router.run()
            ctx.first_run = False
        for player in ctx.tournament.players:
            if player.first_name == name \
               or player.last_name == name:
                assert float(score) == ctx.tournament.player_score(player)
                return
