from .events import EventListener


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


class MainController(Controller):
    def __init__(self):
        super().__init__()

    def on_event(self, event):
        if event.name() == 'activate' and event.get('action') == 'q':
            self._model.quit()
