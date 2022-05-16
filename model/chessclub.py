from .player import Player
from .tournament import Tournament


class ChessClub:
    """Chess club main class"""
    def __init__(self, data_store):
        self._data_store = data_store
        self._running = False

    def run(self):
        self._running = True

    def is_running(self):
        return self._running

    def save(self):
        self._data_store.save()

    def load(self):
        self._data_store.load()

    def new_player(self,
                   last_name,
                   first_name,
                   date_of_birth,
                   gender,
                   ranking):
        """Create a new player and store it inside the data store"""
        p = Player(
            last_name,
            first_name,
            date_of_birth,
            gender,
            ranking)
        self._data_store.store_player(p)
        return p

    def change_player_ranking(self, player, ranking):
        self._data_store.find_players_by_name(player.name).ranking = ranking

    def new_tournament(self,
                       name,
                       place,
                       date,
                       category,
                       description):
        tournament = Tournament(name,
                                place,
                                date,
                                date,
                                category,
                                description)
        self._data_store.store_tournament(tournament)
        return tournament

    def add_tournament(self, tournament):
        self._data_store.store_tournament(tournament)
        return tournament

    def get_all_players(self):
        return self._data_store.players()

    def get_all_tournaments(self):
        return self._data_store.tournaments()

    def quit(self):
        self._running = False
        print('Au revoir !')
