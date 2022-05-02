from .player import Player


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
        self._data_store.store_player(Player(
            last_name,
            first_name,
            date_of_birth,
            gender,
            ranking))

    def quit(self):
        self._running = False
        print('Au revoir !')
