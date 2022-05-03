from behave import given, when, then
from model.chessclub import ChessClub
from model.datastore import DataStore
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


@given('eight players')
def step_impl(ctx):
    user_interactor = MyUserInteractor()
    ctx.io = user_interactor
    data_store = DataStore()
    ctx.data = data_store
    model = ChessClub(data_store)
    factory = XMLFactory(user_interactor)
    view = factory.load_from_file('data/menu.xml')
    router = AppRouter(user_interactor, model, view)
    ctx.router = router
    router.set_controller(MainController())
    ctx.starts = []
    ctx.ends = []

    model.new_player('Kazparov', 'Garry', '12/08/1995', 'M', '0')
    model.new_player('Carlsen', 'Magnus', '12/08/1995', 'M', '1')
    model.new_player('Fischer', 'Bobby', '12/08/1995', 'M', '2')
    model.new_player('Capablanca', 'Jose Raul', '12/08/1995', 'M', '3')
    model.new_player('Karpov', 'Anatoly', '12/08/1995', 'M', '4')
    model.new_player('Botvinnik', 'Mikhail', '12/08/1995', 'M', '5')
    model.new_player('Kramnik', 'Vladimir', '12/08/1995', 'M', '6')
    model.new_player('Lasker', 'Emanuel', '12/08/1995', 'M', '7')

    @when('I enter "{action}"')
    def step_impl(ctx, action):
        ctx.io.add_response(action)

    @when('I enter name "{name}"')
    def step_impl(ctx, name):
        ctx.io.add_response(name)
        ctx.name = name


    @when('I enter place "{place}"')
    def step_impl(ctx, place):
        ctx.io.add_response(place)
        ctx.place = place

    @when('I enter date "{date}"')
    def step_impl(ctx, date):
        ctx.io.add_response(date)
        ctx.date = date

    @when('I enter category "{category}"')
    def step_impl(ctx, category):
        ctx.io.add_response(category)
        ctx.category = category

    @when('I enter description "{description}"')
    def step_impl(ctx, description):
        ctx.io.add_response(description)
        ctx.description = description


    @when('I add player "{index}"')
    def step_impl(ctx, index):
        ctx.io.add_response('j')
        ctx.io.add_response(str(index))

    @when('I add a round from {start} to {end}')
    def step_impl(ctx, start, end):
        ctx.io.add_response('r')
        ctx.io.add_response(str(start))
        ctx.io.add_response(str(end))
        ctx.starts.append(start)
        ctx.ends.append(end)

    @then('the tournament is successfully created')
    def step_impl(ctx):
        ctx.router.run()
        assert 1 == len(ctx.data._tournaments)
        tournament = ctx.data._tournaments[-1]
        assert ctx.name == tournament._name
        assert ctx.place == tournament._place
        assert ctx.date == tournament._start_date
        assert ctx.category == tournament._category
        assert ctx.description == tournament._description
        assert 8 == len(tournament._players)
        assert 'Kazparov' == tournament._players[0].last_name
        assert 'Carlsen' == tournament._players[1].last_name
        assert 'Fischer' == tournament._players[2].last_name
        assert 'Capablanca' == tournament._players[3].last_name
        assert 'Karpov' == tournament._players[4].last_name
        assert 'Botvinnik' == tournament._players[5].last_name
        assert 'Kramnik' == tournament._players[6].last_name
        assert 'Lasker' == tournament._players[7].last_name

        for i in range(0, len(tournament._rounds)):
            assert f'Round {i+1}' == tournament._rounds[i]._name
            assert ctx.starts[i] == tournament._rounds[i]._start.strftime('%d/%m/%y') \
                or ctx.starts[i] == tournament._rounds[i]._start.strftime('%d/%m/%Y')
            assert ctx.ends[i] == tournament._rounds[i]._end.strftime('%d/%m/%y') \
                or ctx.ends[i] == tournament._rounds[i]._end.strftime('%d/%m/%Y')

    @then('the tournament creation failed')
    def step_impl(ctx):
        try:
            ctx.router.run()
            assert False
        except Exception:
            assert 0 == len(ctx.data._tournaments)
                
    @then('{n} tournaments has been created')
    def step_impl(ctx, n):
        ctx.router.run()
        assert int(n) == len(ctx.data._tournaments)
                
