from .errors import ControllerError


class AppController:
    def __init__(self):
        self.controllers = {}
        self.current = None

    def add_controller(self, name, controller):
        self.controllers[name] = controller
        controller.parent = self
        if self.current is None:
            self.current = name

    def current_controller(self):
        if self.current not in self.controllers.keys():
            raise ControllerError('no current controller')
        return self.controllers[self.current]

    def current_controller_name(self):
        if self.current not in self.controllers.keys():
            raise ControllerError('no current controller')
        return self.current

    def goto(self, controller_name):
        if controller_name not in self.controllers.keys():
            raise ControllerError('cannot goto unknown'
                                  f'controller "{controller_name}"')
        self.current = controller_name

    def run(self, iteration_count=-1):
        if self.current is None:
            raise ControllerError('cannot run app without controller')

        self.controllers[self.current].run(iteration_count)
