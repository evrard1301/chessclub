class MatchResult:
    WON = 0
    LOSE = 1
    DRAW = 2


class Match:
    def __init__(self, player_0, player_1):
        self._player_0 = player_0
        self._player_1 = player_1
        self._result = None

    @property
    def players(self):
        return (self._player_0, self._player_1)

    @property
    def result(self):
        return self._result

    def set_result(self, result):
        self._result = result
