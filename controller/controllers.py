
from .events import EventListener
from copy import deepcopy
from datetime import date
from model.match import MatchResult
from model.pairgenerator import SwissPairGenerator
from model.round import Round
from model.tournament import Tournament
import re
from view.menu import StopAndSave


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
        self._play_ctrl = PlayController(self)
        self._setup_ctrl = SetupController(self)
        self._report_ctrl = ReportController(self)

    def on_event(self, event):
        if event.get('action') == 'S':
            self.on_save()

        if event.get('action') == 'C':
            self.on_load()

        if event.get('action') == 'R':
            self._router.set_controller(self._report_ctrl)

        if event.get('action') == 'j':
            self.on_new_player(event)

        if event.get('action') == 'q':
            self._model.quit()

        if event.get('action') == 't':
            self._router.set_controller(self._setup_ctrl)

        if event.get('action') == 'J':
            self._router.set_controller(self._play_ctrl)

        if event.get('action') == 'c':
            next_ctrl = EditRankingController()
            self._router.set_controller(next_ctrl)

    def on_new_player(self, event):
        last_name = self._view.io().ask("Nom de famille: ")
        first_name = self._view.io().ask("Prénom: ")
        date_of_birth = self._view.io().ask("Date de naissance: ")
        date_of_birth_parts = date_of_birth.split('/')
        if not re.match('[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2}',
                        date_of_birth):
            raise MainControllerError('la date de naissance '
                                      'doit être au format '
                                      'jj/mm/aaaa')

        gender = self._view.io().ask("Genre: ")
        if gender.strip(' ') != gender:
            raise MainControllerError('le genre doit avoir une valeur')

        ranking = self._view.io().ask("Rang: ")
        if not re.match('[0-9]+', ranking):
            raise MainControllerError('le rang doit être un nombre')

        save = self._view.io().ask("Sauvegarder ? (O/n) ")

        if save.lower() == 'o':
            self._model.new_player(last_name,
                                   first_name,
                                   date(int(date_of_birth_parts[2]),
                                        int(date_of_birth_parts[1]),
                                        int(date_of_birth_parts[0])),
                                   gender,
                                   ranking)

    def on_save(self):
        self._model.save()

    def on_load(self):
        self._model.load()


class SetupController(Controller):
    def __init__(self, main_ctrl):
        super().__init__()
        self._main_ctrl = main_ctrl
        self._tournament = Tournament(
            '',
            '',
            '',
            '',
            '',
            ''
        )

    def on_event(self, event):
        try:
            if event.get('action') == 'q':
                self._router.set_controller(self._main_ctrl)

            if event.get('action') == 'i':
                self._ask_informations()

            if event.get('action') == 'v':
                self._view_informations()

            if event.get('action') == 'j':
                self._add_player()

            if event.get('action') == 'l':
                self._list_players()

            if event.get('action') == 'r':
                self._add_round()

            if event.get('action') == 't':
                self._create()
        except StopAndSave:
            pass

    def _input(self, msg):
        value = self._view.io().ask(msg)
        if value == '\\quitter':
            raise StopAndSave()
        return value

    def _ask_informations(self):
        name = self._input('Nom: ')
        self._tournament._name = name

        place = self._input('Lieu: ')
        self._tournament._place = place
        the_date = self._input('Date: ')
        self._tournament._start_date = the_date
        self._tournament._end_date = the_date

        time_setting = self._input('Paramètre temps (BULLET'
                                   '/blitz/rapide)')
        if not re.match('bullet|blitz|rapide',
                        time_setting.lower()):
            raise MainControllerError('La catégorie "'
                                      + time_setting
                                      + '" est invalide')
        self._tournament._category = time_setting

        description = self._input('Description: ')
        self._tournament._description = description

    def _view_informations(self):
        self._view.io().tell('Résumé')
        self._view.io().tell('-------- Informations --------')
        self._view.io().tell(f'Nom: {self._tournament._name}')
        self._view.io().tell(f'Lieu: {self._tournament._place}')
        self._view.io().tell(f'Date: {self._tournament._start_date}')
        self._view.io().tell(f'Paramètre: {self._tournament._category}')
        self._view.io().tell(f'Description: {self._tournament._description}')

        self._view.io().tell('-------- Joueurs --------')

        for player in self._tournament.players:
            self._view.io().tell(f'{player.first_name}'
                                 f' {player.last_name}')

        self._view.io().tell('-------- Tours --------')
        for i in range(0, len(self._tournament.rounds), 2):
            print(f'Tour {int(i/2)}: du'
                  f' {self._tournament.rounds[i]} au'
                  f' {self._tournament_rounds[i+1]}')

    def _add_player(self):
        player_id = int(self._input('ID du joueur: '))
        player = self._model.get_all_players()[player_id]
        self._tournament.add_player(player)
        self._view.io().tell(f'{player.name} a été ajouté au tournoi')

    def _list_players(self):
        for i, player in enumerate(self._model.get_all_players()):
            self._view.io().tell(f'Player {i}: {player.name}')

    def _add_round(self):
        start_date_str = self._input('Date de début: ')
        start_date_split = start_date_str.split('/')
        start_date = date(int(start_date_split[2]),
                          int(start_date_split[1]),
                          int(start_date_split[0]))

        end_date_str = self._input('Date de fin: ')
        end_date_split = end_date_str.split('/')
        end_date = date(int(end_date_split[2]),
                        int(end_date_split[1]),
                        int(end_date_split[0]))

        num = len(self._tournament.rounds) + 1
        my_round = Round(f'Round {num}', start_date, end_date)
        self._tournament.add_round(my_round)
        self._view.io().tell(f'{my_round.name} a été ajouté au tournoi')

    def _create(self):

        if len(self._tournament.players) != 8:
            raise MainControllerError('Le tournoi doit comporter huit joueurs'
                                      ' (et non pas '
                                      f'{len(self._tournament.players)}.)')

        for i, player_0 in enumerate(self._tournament.players):
            for j, player_1 in enumerate(self._tournament.players):
                if j > i and player_0.same_as(player_1):
                    raise MainControllerError(f'Le joueur {player_0.name} est '
                                              'déjà présent dans le tournoi')

        if len(self._tournament.rounds) == 0:
            raise MainControllerError('Le tournoi doit être composé d\'au'
                                      ' moins un round')

        for i, my_round_0 in enumerate(self._tournament.rounds):
            for j, my_round_1 in enumerate(self._tournament.rounds):
                if i != j \
                   and my_round_0.start > my_round_1.start \
                   and my_round_0.start < my_round_1.end:
                    raise MainControllerError('Un tour ne peux pas '
                                              'commencer lorsque un tour')

        self._model.add_tournament(self._tournament)
        self._view.io().tell('Le tournoi a été crée')

        self._tournament = Tournament(
            '',
            '',
            '',
            '',
            '',
            ''
        )


class PlayController(Controller):
    class LastState:
        def __init__(self, pairs, index, results):
            self.pairs = pairs
            self.index = index
            self.results = results

    def __init__(self, main_ctrl):
        super().__init__()
        self._tournament_id = None
        self._main_ctrl = main_ctrl

        self._last_state = None

    def on_event(self, event):
        if event.get('action') == 'q':
            self._router.set_controller(MainController())
        elif event.get('action') == 'c':
            self._tournament_id = int(self._view.io().ask('ID du tournois: '))
            tournament = self._model.get_all_tournaments()[self._tournament_id]
            confirm = self._view.io().ask('Jouer le tournoi '
                                          f'"{tournament.name}"'
                                          ' (o/N): ').lower()
            if confirm != 'o':
                self._tournament_id = None
        elif event.get('action') == 'l':
            id = 0
            self._view.io().tell('ID | Nom')
            self._view.io().tell('--------')
            for tournament in self._model.get_all_tournaments():
                self._view.io().tell(str(id) + ' ' + tournament.name)
                id += 1
        elif event.get('action') == 'j':
            if self._tournament_id is not None:
                try:
                    self.play()
                except StopAndSave:
                    self._router.reset_session()
                    self._router.set_controller(self._main_ctrl)

    def play(self):
        tournament = self._model.get_all_tournaments()[self._tournament_id]
        gen = SwissPairGenerator()

        while tournament.is_finished() is False:
            self._view.io().tell('\n\n-------- '
                                 f'{tournament.current_round().name} --------')

            pairs = gen.generate(tournament)
            results = []
            start_index = 0

            if self._last_state is not None:
                pairs = self._last_state.pairs
                start_index = self._last_state.index
                results = self._last_state.results

            for i in range(start_index, len(pairs)):
                pair = pairs[i]
                self._view.io().tell(f'\nMatch: {pair[0].name} '
                                     f'contre {pair[1].name}')
                res = self._view.io().ask('Résultat du match '
                                          f'(0: {pair[0].name}, '
                                          f'1: {pair[1].name}, '
                                          '2: match nul): ')
                if res == '\\quitter':
                    self._last_state = self.LastState(pairs, i, results)
                    raise StopAndSave()
                elif res == "0":
                    results.append(MatchResult.WON)
                elif res == "1":
                    results.append(MatchResult.LOSE)
                else:
                    results.append(MatchResult.DRAW)

            tournament.play_round(pairs, results)
            self._last_state = None

        self._view.io().tell('Fin du tournoi !')
        self._view.io().tell('Voici les scores des joueurs')

        self._show_scores(tournament)

    def _show_scores(self, tournament):
        players = deepcopy(self._model.get_all_players())
        players.sort(reverse=True, key=lambda p: tournament.player_score(p))
        for player in players:
            self._view.io().tell(f'{tournament.player_score(player)}\t'
                                 f'{player.name}')


class EditRankingController(Controller):
    def __init__(self):
        super().__init__()
        self._menu = None

    def on_event(self, event):
        players = sorted(self._model.get_all_players(),
                         key=lambda p: p.ranking)

        if event.get('action') == 'q':
            self._router.set_controller(MainController())

        elif event.get('action') == 'v':
            self._show_ranking(players)

        elif event.get('action') == 'm':
            self._change_ranking(players)

    def _show_ranking(self, players):
        self._view.io().tell('RANG -> NOM')
        self._view.io().tell('-----------')
        for player in players:
            self._view.io().tell(f'{player.ranking} -> {player.name}')

    def _change_ranking(self, players):
        for player in players:
            ranking = self._view.io().ask(f'Rang pour {player.name}: ')
            self._model.change_player_ranking(player, ranking)


class ReportController(Controller):
    def __init__(self, main_ctrl):
        self._main_ctrl = main_ctrl

    def on_event(self, event):
        if event.get('action') == 'q':
            self._router.set_controller(self._main_ctrl)
        if event.get('action') == 'a':
            self.report_actors_by_name()
        if event.get('action') == 'A':
            self.report_actors_by_ranking()
        if event.get('action') == 't':
            self.report_actors_by_name(self._ask_tournament())
        if event.get('action') == 'T':
            self.report_actors_by_ranking(self._ask_tournament())

    def report_actors_by_name(self, tournament=None):
        actors_by_name = None
        if tournament is None:
            actors_by_name = deepcopy(self._all_actors())
        else:
            actors_by_name = deepcopy(self._all_tournament_actors(tournament))

        actors_by_name.sort(key=lambda p: p.last_name)

        self._view.io().tell('Prénom \t Nom')
        self._view.io().tell('------------------------')
        for a in actors_by_name:
            self._view.io().tell(a.name)

    def report_actors_by_ranking(self, tournament=None):
        actors_by_ranking = None
        if tournament is None:
            actors_by_ranking = deepcopy(self._all_actors())
        else:
            actors_by_ranking = deepcopy(self._all_tournament_actors(
                tournament
            ))

        actors_by_ranking.sort(key=lambda p: p.ranking)

        self._view.io().tell('Classement' + '\t' + 'Nom')
        self._view.io().tell('------------------------')

        for a in actors_by_ranking:
            self._view.io().tell(a.ranking + '\t' + a.name)

    def _all_actors(self):
        tournaments = self._model.get_all_tournaments()
        players = []
        for tournament in tournaments:
            for player in tournament.players:
                if player.name not in [p.name for p in players]:
                    players.append(player)
        return players

    def _all_tournament_actors(self, tournament):
        players = []
        for player in tournament.players:
            if player.name not in [p.name for p in players]:
                players.append(player)
        return players

    def _ask_tournament(self):
        for i, t in enumerate(self._model.get_all_tournaments()):
            self._view.io().tell(f'{i} -> {t.name}')
        
        myid = int(self._view.io().ask('Quel tournoi '
                                       'voulez-vous sélectionner ? '))
        
        return self._model.get_all_tournaments()[myid]
        
