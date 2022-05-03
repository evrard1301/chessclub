class Tournament:
    def __init__(self,
                 name,
                 place,
                 start_date,
                 end_date,
                 category,
                 description):
        self._name = name
        self._place = place
        self._start_date = start_date
        self._end_date = end_date
        self._category = category
        self._description = description
        self._players = []
        self._rounds = []

    @property
    def rounds(self):
        return self._rounds

    def add_round(self, round):
        self._rounds.append(round)

    def add_rounds(self, rounds):
        for r in rounds:
            self._rounds.append(r)

    def add_players(self, players):
        for p in players:
            self._players.append(p)
