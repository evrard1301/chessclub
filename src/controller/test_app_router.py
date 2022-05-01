from . import Controller, ControllerError, AppController


def test_change_controller():
    app = AppController()
    app.add_controller('first', Controller(None, None))
    app.add_controller('second', Controller(None, None))

    assert 'first' == app.current_controller_name()
    app.goto('second')
    assert 'second' == app.current_controller_name()
    app.goto('first')
    assert 'first' == app.current_controller_name()
    try:
        app.goto('third')
        assert False
    except ControllerError:
        pass
