from view.menu import MenuSession


class AppRouter:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._session = MenuSession(self._view)
        self._controller = None

    def set_controller(self, ctrl):
        if self._controller is not None:
            self._session.remove_listener(self._controller)
        self._controller = ctrl
        self._controller.prepare(self, self._model, self._view)
        self._session.add_listener(ctrl)

    def run(self):
        while True:
            self._session.menu().show()
            self._session.nav(input('> '))

    def goto(self, controller):
        self._controller = controller
