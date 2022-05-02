from behave import given, when, then
from model.chessclub import ChessClub
from model.datastore import DataStore
from view.factory import XMLFactory
from view.userinput import UserInput
from view.menu import MenuError
from controller.approuter import AppRouter
from controller.controllers import MainController, MainControllerError


class MyDataStore(DataStore):
    def __init__(self):
        super().__init__()
        self._player = None

    def store_player(self, player):
        self._player = player

    def player(self):
        return self._player


class MyUserInput(UserInput):
    def __init__(self):
        super().__init__()
        self._inputs = []

    def ask(self, msg):
        if len(self._inputs) == 0:
            raise Exception(f'cannot answer to "{msg}"')
        resp = self._inputs[0]
        if len(self._inputs) > 1:
            del self._inputs[0]
        return resp

    def add(self, input_value):
        self._inputs.append(input_value)

@given('a new session')
def step_impl(ctx):
    ctx.user_input = MyUserInput()
    factory = XMLFactory(ctx.user_input)
    ctx.data_store = MyDataStore()
    model = ChessClub(ctx.data_store)
    view = factory.load_from_file("data/menu.xml")

    ctx.router = AppRouter(ctx.user_input, model, view)
    ctx.router.set_controller(MainController())

@when('I select "{action}"')
def step_impl(ctx, action):
    ctx.user_input.add(action)


@when('I set the last name to be "{lastname}"')
def step_impl(ctx, lastname):
    ctx.user_input.add(lastname)
    ctx.lastname = lastname


@when('I set the first name to be "{firstname}"')
def step_impl(ctx, firstname):
    ctx.user_input.add(firstname)
    ctx.firstname = firstname


@when('I set the date of birth to be "{date}"')
def step_impl(ctx, date):
    ctx.user_input.add(date)
    ctx.date = date


@when('I set the gender to be "{gender}"')
def step_impl(ctx, gender):
    ctx.user_input.add(gender)
    ctx.gender = gender

@when('I set the ranking to be "{ranking}"')
def step_impl(ctx, ranking):
    ctx.user_input.add(ranking)
    ctx.ranking = ranking

@then('a new player is created')
def step_impl(ctx):
    ctx.user_input.add('o')
    ctx.user_input.add('q')    
    ctx.router.run()
    player = ctx.data_store.player()
    assert player.last_name == ctx.lastname
    assert player.first_name == ctx.firstname
    assert player.date_of_birth == ctx.date
    assert player.gender == ctx.gender
    assert player.ranking == ctx.ranking


@then('an error is raised')
def step_impl(ctx):
    ctx.user_input.add('o')
    ctx.user_input.add('q')
    try:
        ctx.router.run()
        assert False
    except MainControllerError:
        assert True
    except Exception:
        assert False
    
