from abc import ABC
from abc import abstractmethod
from view.menu import MenuSession


class AppErrorManager(ABC):
    def __init__(self, user_interactor):
        self._user_interactor = user_interactor

    @abstractmethod
    def on_error(self, err):
        pass


class RaiseErrorManager(AppErrorManager):
    def on_error(self, err):
        raise err


class PrintErrorManager(AppErrorManager):
    def on_error(self, err):
        print(err)


class AppRouter:
    def __init__(self, user_interactor, model, view):
        self._user_interactor = user_interactor
        self._model = model
        self._view = view
        self._session = MenuSession(self._view)
        self._controller = None
        self._error_manager = RaiseErrorManager(self._user_interactor)

    def set_error_manager(self, error_manager):
        self._error_manager = error_manager

    def set_controller(self, ctrl):
        if self._controller is not None:
            self._session.remove_listener(self._controller)
        self._controller = ctrl
        self._controller.prepare(self, self._model, self._view)
        self._session.add_listener(ctrl)

    def reset_session(self):
        self._session = MenuSession(self._view)
        self._session.add_listener(self._controller)

    def run(self):
        self._model.run()
        while self._model.is_running():
            try:
                self._session.menu().show()
                self._session.nav(self._user_interactor.ask('> '))
            except Exception as err:
                self._error_manager.on_error(err)

    def goto(self, controller):
        self._controller = controller
