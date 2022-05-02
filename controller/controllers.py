from .events import EventListener
from model.round import Round
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
        self.reset()

    def reset(self):
        self._player_info = []
        self._tournament_info = []
        self._tournament_players = []
        self._tournament_rounds = []
        self._menu = None

    def on_event(self, event):
        if event.name() == 'activate' and event.get('action') == 'q':
            self._model.quit()

        if event.name() == 'ask':
            if event.get('action') == 'j':
                self.on_new_player(event)
        if event.name() == 'goto':
            self._menu = event.get('menu')

        elif self._menu is not None and self._menu.title == 'Nouveau tournoi':
            self.on_new_tournament(event)

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

    def on_new_tournament(self, event):
        all_players = self._model.get_all_players()

        if event.get('action') == 't':
            t = self._model.new_tournament(self._tournament_info[0],
                                           self._tournament_info[1],
                                           self._tournament_info[2],
                                           self._tournament_info[3],
                                           self._tournament_info[4])
            t.add_players(self._tournament_players)
            for i in range(0, len(self._tournament_rounds), 2):
                t.add_round(Round(f'Round {int(i/2)+1}',
                                  self._tournament_rounds[i],
                                  self._tournament_rounds[i+1]))

            self.reset()
        if event.get('action') == 'l':
            index = 0
            self._view.io().tell('ID | Prénom | Nom')
            self._view.io().tell('-------------------------')
            for player in all_players:
                self._view.io().tell(
                    f'[{index}] | '
                    f'{player.first_name} | '
                    f'{player.last_name} ')
                index += 1

        if event.get('action') == 'v':
            self._view.io().tell('Résumé')
            self._view.io().tell('-------- Informations --------')
            for info in self._tournament_info:
                self._view.io().tell(info)

            self._view.io().tell('-------- Joueurs --------')
            for player in self._tournament_players:
                self._view.io().tell(f'{player.first_name}'
                                     f' {player.last_name}')
            self._view.io().tell('-------- Tours --------')
            for i in range(0, len(self._tournament_rounds), 2):
                print(f'Tour {int(i/2)}: du'
                      f' {self._tournament_rounds[i]} au'
                      f' {self._tournament_rounds[i+1]}')
        if event.name() == 'ask':
            if event.get('question').text() == 'ID du joueur':
                player = all_players[int(event.get('response'))]
                self._tournament_players.append(player)
                self._view.io().tell('Ajout du joueur'
                                     f' {player.first_name}'
                                     f' {player.last_name}')
            elif event.get('question').text() == 'Date de début':
                self._tournament_rounds.append(event.get('response'))
            elif event.get('question').text() == 'Date de fin':
                self._tournament_rounds.append(event.get('response'))
            else:
                if event.get('index') == 1:
                    self._tournament_info.clear()
                self._tournament_info.append(event.get('response'))
