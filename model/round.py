from model.match import MatchResult


class Round:
    def __init__(self, name, start, end):
        self._name = name
        self._start = start
        self._end = end
        self._matches = []

    @property
    def name(self):
        return self._name

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def during_round(self, a_date):
        return a_date > self._start and a_date < self._end

    def add_match(self, match):
        self._matches.append(match)

    def player_score(self, player):
        score = 0
        for match in self._matches:
            p0, p1 = match.players

            if player.same_as(p0):
                if match.result == MatchResult.WON:
                    score += 1
                elif match.result == MatchResult.DRAW:
                    score += 0.5
            elif player.same_as(p1):
                if match.result == MatchResult.LOSE:
                    score += 1
                elif match.result == MatchResult.DRAW:
                    score += 0.5
        return score

    def find_matches_by_players(self, player_0, player_1):
        matches = []
        for match in self._matches:
            p, q = match.players
            if p.same_as(player_0) and q.same_as(player_1) \
               or p.same_as(player_1) and q.same_as(player_0):
                matches.append(match)
        return matches
