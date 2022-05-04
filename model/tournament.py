from model.match import Match


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
        self._current_round = 0

    def is_finished(self):
        if self._current_round is None:
            return True
        return self._current_round >= len(self._rounds)

    @property
    def name(self):
        return self._name

    @property
    def players(self):
        return self._players

    @property
    def rounds(self):
        return self._rounds

    def current_round(self):
        if self._current_round is None:
            return None
        return self._rounds[self._current_round]

    def previous_round(self):
        if self._current_round is None or self._current_round == 0:
            return None
        return self._rounds[self._current_round - 1]

    def add_round(self, round):
        self._rounds.append(round)

    def add_rounds(self, rounds):
        for r in rounds:
            self._rounds.append(r)

    def add_player(self, player):
        self._players.append(player)

    def add_players(self, players):
        for p in players:
            self._players.append(p)

    def play_round(self, player_pairs, results):
        if self._current_round is None:
            self._current_round = 0

        my_round = self._rounds[self._current_round]
        i = 0

        for result in results:
            m = Match(player_pairs[i][0], player_pairs[i][1])
            m.set_result(result)
            my_round.add_match(m)
            i += 1
        self._current_round += 1

    def player_score(self, player):
        score = 0
        for my_round in self._rounds:
            score += my_round.player_score(player)
        return score

    def is_first_round(self):
        return self._current_round is None
