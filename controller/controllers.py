from .events import EventListener
from copy import deepcopy
from datetime import date
from model.match import MatchResult
from model.pairgenerator import SwissPairGenerator
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
        self._player_info = []

    def on_event(self, event):
        if event.name() == 'activate' and event.get('action') == 'q':
            self._model.quit()

        if event.name() == 'ask':
            if event.get('action') == 'j':
                self.on_new_player(event)
            if event.get('action') == 'q':
                self._model.quit()

        if event.name() == 'goto' and event.get('action') == 't':
            next_ctrl = SetupController()
            self._router.set_controller(next_ctrl)

        if event.name() == 'goto' and event.get('action') == 'J':
            next_ctrl = PlayController()
            self._router.set_controller(next_ctrl)

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
            date_of_birth_parts = self._player_info[2].split('/')
            self._model.new_player(self._player_info[0],
                                   self._player_info[1],
                                   date(int(date_of_birth_parts[2]),
                                        int(date_of_birth_parts[1]),
                                        int(date_of_birth_parts[0])),
                                   self._player_info[3],
                                   self._player_info[4])
            self._player_info.clear()
        else:
            self._player_info.clear()


class SetupController(Controller):
    def __init__(self):
        super().__init__()
        self.reset()
        self._menu = None

    def reset(self):
        self._tournament_info = []
        self._tournament_players = []
        self._tournament_rounds = []

    def on_event(self, event):
        if event.name() == 'goto' and event.get('action') == 'q':
            self._router.set_controller(MainController())

        self.on_new_tournament(event)

    def on_new_tournament(self, event):
        all_players = self._model.get_all_players()
        self.tournament_create(event, all_players)
        self.tournament_show_players(event, all_players)
        self.tournament_show_results(event, all_players)
        self.tournament_update_info(event, all_players)

    def tournament_create(self, event, all_players):
        if event.get('action') == 't':
            if not re.match('bullet|blitz|rapide',
                            self._tournament_info[3].lower()):
                raise MainControllerError('La catégorie "'
                                          + self._tournament_info[3]
                                          + '" est invalide')
            for i in range(0, len(self._tournament_players)):
                for j in range(i + 1, len(self._tournament_players)):
                    if self._tournament_players[i] \
                       == self._tournament_players[j]:
                        raise MainControllerError('Le joueur ',
                                                  self._tournament_players[i],
                                                  'apparait deux fois '
                                                  'dans le tournoi')
            if len(self._tournament_rounds) == 0:
                raise MainControllerError('Le tournoi doit posséder'
                                          ' au moins un tour')
            if len(self._tournament_players) != 8:
                raise MainControllerError('Le tournoi doit accueillir'
                                          ' huit joueurs')

            rounds = []
            for i in range(0, len(self._tournament_rounds), 2):
                start_parts = self._tournament_rounds[i].split('/')
                end_parts = self._tournament_rounds[i+1].split('/')
                start = date(int(start_parts[2]),
                             int(start_parts[1]),
                             int(start_parts[0]))
                end = date(int(end_parts[2]),
                           int(end_parts[1]),
                           int(end_parts[0]))

                rounds.append(Round(f'Round {int(i/2)+1}', start, end))

            for i in range(0, len(rounds)):
                r0 = rounds[i]
                for j in range(i + 1, len(rounds)):
                    r1 = rounds[j]
                    if r0.during_round(r1.start) or r0.during_round(r1.end):
                        raise MainControllerError(f'{r1.name} ne devrait pas '
                                                  'se dérouler '
                                                  f'pendant {r0.name}')

            t = self._model.new_tournament(self._tournament_info[0],
                                           self._tournament_info[1],
                                           self._tournament_info[2],
                                           self._tournament_info[3],
                                           self._tournament_info[4])

            t.add_players(self._tournament_players)

            if start > end:
                raise MainControllerError('la date de début du tour'
                                          'doit être antérieur '
                                          'à la date de fin')

            for r in rounds:
                t.add_round(r)

            self._view.io().tell('Le tournoi a bien été crée')
            self.reset()

    def tournament_show_players(self, event, all_players):
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

    def tournament_show_results(self, event, all_players):
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

    def tournament_update_info(self, event, all_players):
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


class PlayController(Controller):
    def __init__(self):
        super().__init__()
        self._responses = []

    def on_event(self, event):
        if event.name() == 'ask':
            self._responses.append(event.get('response'))

        if event.get('action') == 'q':
            self._router.set_controller(MainController())
        elif event.get('action') == 'l':
            id = 0
            self._view.io().tell('ID | Nom')
            self._view.io().tell('--------')
            for tournament in self._model.get_all_tournaments():
                self._view.io().tell(str(id) + ' ' + tournament.name)
                id += 1
        elif event.get('action') == 'j':
            if len(self._responses) == 2 \
               and self._responses[1].lower() == 'o':
                self.play()

    def play(self):
        tournament = self._model.get_all_tournaments()[int(self._responses[0])]
        gen = SwissPairGenerator()

        while tournament.is_finished() is False:
            self._view.io().tell('\n\n-------- '
                                 f'{tournament.current_round().name} --------')
            pairs = gen.generate(tournament)
            results = []
            for pair in pairs:
                self._view.io().tell(f'\nMatch: {pair[0].name} '
                                     f'contre {pair[1].name}')
                res = self._view.io().ask('Résultat du match '
                                          f'(0: {pair[0].name}, '
                                          f'1: {pair[1].name}, '
                                          '2: match nul): ')
                if res == "0":
                    results.append(MatchResult.WON)
                elif res == "1":
                    results.append(MatchResult.LOSE)
                else:
                    results.append(MatchResult.DRAW)

            tournament.play_round(pairs, results)
            self._show_scores(tournament)

        self._view.io().tell('Fin du tournoi !')
        self._view.io().tell('Voici les scores des joueurs')

        self._show_scores(tournament)

    def _show_scores(self, tournament):
        players = deepcopy(self._model.get_all_players())
        players.sort(reverse=True, key=lambda p: tournament.player_score(p))
        for player in players:
            self._view.io().tell(f'{tournament.player_score(player)}\t'
                                 f'{player.name}')
