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

    def new_tournament(self,
                       name,
                       place,
                       date,
                       category,
                       description):
        tournament = Tournament(name,
                                place,
                                date,
                                category,
                                description)
        self._data_store.store_tournament(tournament)
        return tournament

    def get_all_players(self):
        return self._data_store.players()

    def quit(self):
        self._running = False
        print('Au revoir !')
