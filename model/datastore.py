import datetime
from model.match import Match
from model.player import Player
from model.round import Round
from model.tournament import Tournament
import tinydb


class DataStore:
    def __init__(self):
        self._players = []
        self._tournaments = []

    def save(self):
        raise NotImplementedError('cannot save')

    def load(self):
        raise NotImplementedError('cannot load')

    def store_player(self, player):
        self._players.append(player)

    def store_tournament(self, tournament):
        self._tournaments.append(tournament)

    def players(self):
        return self._players

    def tournaments(self):
        return self._tournaments

    def find_players_by_ranking(self, ranking):
        return [p for p in self._players if int(p.ranking) == int(ranking)]

    def find_players_by_name(self, name):
        return [p for p in self._players if p.name == name][0]


class TinyDBStore(DataStore):
    def __init__(self):
        self._players = []
        self._tournaments = []
        self._db = tinydb.TinyDB('db.json')

    def save(self):
        player_table = self._db.table('Player')
        player_table.truncate()
        for player in self._players:
            player_table.insert(player.__dict__)

        tournament_table = self._db.table('Tournament')
        tournament_table.truncate()
        for tournament in self._tournaments:
            print(tournament.__dict__)
            tournament_table.insert(tournament.__dict__)

    def load(self):
        player_table = self._db.table('Player')

        for p in player_table.all():
            self.store_player(Player(
                p['last_name'],
                p['first_name'],
                p['date_of_birth'],
                p['gender'],
                p['ranking']
            ))

        tournament_table = self._db.table('Tournament')
        for t in tournament_table.all():
            the_tournament = Tournament('', '', '', '', '', '')
            the_tournament._name = t['name']
            the_tournament._place = t['place']
            the_tournament._start_date = t['start_date']
            the_tournament._end_date = t['end_date']
            the_tournament._category = t['category']
            the_tournament._description = t['description']
            the_tournament._current_round = t['current_round']

            for name in t['players']:
                the_tournament.add_player(self.find_players_by_name(name))

            for r in t['rounds']:
                the_round = Round(r['name'],
                                  datetime.date(*[
                                      int(i)
                                      for i in r['start'].split('-')
                                  ]),
                                  datetime.date(*[
                                      int(i)
                                      for i in r['end'].split('-')
                                  ]))

                for match in r['matches']:
                    m = Match(self.find_players_by_name(match['player_0']),
                              self.find_players_by_name(match['player_1']))
                    m.set_result(int(match['result']))
                    the_round.add_match(m)

                the_tournament.add_round(the_round)

            self._tournaments.append(the_tournament)

    def store_player(self, player):
        self._players.append(player)

    def store_tournament(self, tournament):
        self._tournaments.append(tournament)

    def players(self):
        return self._players

    def tournaments(self):
        return self._tournaments

    def find_players_by_ranking(self, ranking):
        return [p for p in self._players if int(p.ranking) == int(ranking)]

    def find_players_by_name(self, name):
        return [p for p in self._players if p.name == name][0]
