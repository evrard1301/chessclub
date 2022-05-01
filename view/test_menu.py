import pytest
from .menu import Menu, MenuSession, MenuError


def test_nav():
    menu_0 = Menu('First Menu')
    menu_1 = Menu('Second Menu')

    menu_1.add(Menu('First'), 'd')
    menu_1.add(Menu('Second'), 'e')
    menu_1.add(Menu('Last'), 'f')
    menu_1.add(menu_0, 'p')

    menu_0.add(Menu('First'), 'a')
    menu_0.add(Menu('Second'), 'b')
    menu_0.add(Menu('Last'), 'c')
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
    menu = Menu('First')
    menu.add(Menu('Option'), 'o')
    session = MenuSession(menu)

    with pytest.raises(MenuError):
        session.nav('p')
