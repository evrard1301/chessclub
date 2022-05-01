from .events import EventListener


class Controller(EventListener):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.parent = None
        self.view.add_listener(self)
        
    def on_event(self, event):
        raise NotImplementedError()

    def run(self, iteration_count=-1):
        raise NotImplementedError()


class MainController(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)

    def on_event(self, event):
        if event.name == 'goto_entry':
            if event.args['entry'].action == 'q':
                exit(0)

    def run(self, iteration_count=-1):
        session = self.view.session()

        itr = 0

        while itr < iteration_count or iteration_count == -1:
            session.show()
            user_response = input("> ")
            session.goto(user_response)
            itr += 1


class SetupController(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)

    def on_event(self, event):
        pass

    def run(self, iteration_count=-1):
        session = self.view.session()

        itr = 0

        while itr < iteration_count or iteration_count == -1:
            session.show()
            user_response = input("> ")
            session.goto(user_response)
            itr += 1
