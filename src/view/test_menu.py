from view.menu import Menu, MenuError


def test_menu_navigation():
    test_menu_navigation.called = False

    def callback():
        test_menu_navigation.called = True

    menu_opt = Menu('options')
    menu_opt.add_entry('v', 'video')
    menu_opt.add_entry('a', 'audio', callback)
    menu_opt.add_entry('c', 'controls')

    menu = Menu('main')
    menu.add_entry('p', 'play')
    menu.add_menu('o', menu_opt)
    menu.add_entry('q', 'quit')

    s = menu.session()
    assert test_menu_navigation.called is False
    s.goto('o')
    assert test_menu_navigation.called is False
    s.goto('a')
    assert test_menu_navigation.called is True


def test_invalid_menu_navigation():
    menu = Menu('main')
    menu.add_entry('p', 'play')
    menu.add_entry('o', 'options')
    menu.add_entry('q', 'quit')

    try:
        s = menu.session()
        s.goto('k')
        assert False
    except MenuError:
        pass
    except Exception:
        assert False
