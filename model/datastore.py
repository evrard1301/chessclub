class DataStore:
    def __init__(self):
        self._players = []
        self._tournaments = []

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
