from .menu import Menu
from .menu import MenuError
from .menu import MenuInput
from .menu import MenuSession
from .userinteractor import ConsoleUserInteractor
import pytest


def test_nav():
    user_interactor = ConsoleUserInteractor()
    menu_0 = Menu('First Menu', user_interactor)
    menu_1 = Menu('Second Menu', user_interactor)

    menu_1.add(Menu('First', user_interactor), 'd')
    menu_1.add(Menu('Second', user_interactor), 'e')
    menu_1.add(Menu('Last', user_interactor), 'f')
    menu_1.add(menu_0, 'p')

    menu_0.add(Menu('First', user_interactor), 'a')
    menu_0.add(Menu('Second', user_interactor), 'b')
    menu_0.add(Menu('Last', user_interactor), 'c')
    menu_0.add(menu_1, 'n')

    session = MenuSession(menu_0)
    assert menu_0 == session.menu()
    session.nav('a')
    assert menu_0 == session.menu()
    session.nav('n')
    assert menu_1 == session.menu()
    session.nav('p')
    assert menu_0 == session.menu()


def test_wrong_action():
    user_interactor = ConsoleUserInteractor()
    menu = Menu('First', user_interactor)
    menu.add(Menu('Option', user_interactor), 'o')
    session = MenuSession(menu)

    with pytest.raises(MenuError):
        session.nav('p')


def test_input():
    test_input.called = False

    class MenuInputMock(MenuInput):
        def ask(self):
            test_input.called = True
            return 'toto'
    user_interactor = ConsoleUserInteractor()
    menu = Menu('my menu', user_interactor)
    menu.add_input('a', MenuInputMock('coucou', 'txt'))
    menu.add('hola', 'a')
    menu.add('mec', 'b')
    session = MenuSession(menu)
    session.nav('b')
    assert session[0] is None
    assert test_input.called is False
    session.nav('a')
    assert test_input.called is True
    assert 'toto' == session[0]
