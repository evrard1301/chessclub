class DataStore:
    def __init__(self):
        self._players = []

    def store_player(self, player):
        self._players.append(player)
