from .events import EventListener
import re


class Controller(EventListener):
    def __init__(self):
        super().__init__()
        self._router = None
        self._model = None
        self._view = None

    def prepare(self, router, model, view):
        """Prepare the controller to be used by the router."""
        self._router = router
        self._model = model
        self._view = view


class MainControllerError(Exception):
    pass


class MainController(Controller):
    def __init__(self):
        super().__init__()
        self._player_info = []

    def on_event(self, event):
        if event.name() == 'activate' and event.get('action') == 'q':
            self._model.quit()

        if event.name() == 'ask':
            if event.get('action') == 'j':
                self.on_new_player(event)

    def on_new_player(self, event):
        if len(self._player_info) < event.get('count') - 1:
            self._player_info.append(event.get('response'))
            if event.get("index") == 3:
                if not re.match('[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2}',
                                event.get('response')):
                    raise MainControllerError('la date de naissance '
                                              'doit être au format '
                                              'jj/mm/aaaa')
            if event.get("index") == 5:
                if not re.match('[0-9]+',
                                event.get('response')):
                    raise MainControllerError('le rang doit être un nombre')
            if self._player_info[-1].strip() == '':
                raise MainControllerError('champs invalide')
        elif event.get('response').lower() == 'o':
            self._model.new_player(self._player_info[0],
                                   self._player_info[1],
                                   self._player_info[2],
                                   self._player_info[3],
                                   self._player_info[4])
            self._player_info.clear()
        else:
            self._player_info.clear()
