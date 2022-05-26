from abc import ABC
from abc import abstractmethod
import copy


class PairGenerator(ABC):
    @abstractmethod
    def generate(self, tournament):
        pass


class SwissPairGenerator(PairGenerator):
    def __init__(self):
        pass

    def generate(self, tournament):
        if tournament.is_first_round():
            return self._generate_first_round(tournament)
        return self._generate(tournament)

    def _generate_first_round(self, tournament):
        players = copy.copy(tournament.players)
        result = []

        players.sort(key=lambda p: int(p.ranking))

        i = 0
        total = int(len(players)/2)

        while i < total:
            result.append((players[i], players[total + i]))
            i += 1

        return result

    def _generate_from_scores(self, tournament, player_scores):
        players = copy.copy(tournament.players)
        result = []

        players.sort(reverse=True, key=lambda p: player_scores[p.name])

        while len(players) > 0:
            p0 = 0
            p1 = 1

            my_round = tournament.previous_round()
            if my_round is not None:
                while True:
                    matches = tournament.find_matches_by_players(players[p0],
                                                                 players[p1])
                    if len(matches) > 0:
                        p1 += 1
                    else:
                        break

            result.append((players[p0], players[p1]))

            del players[p0]
            del players[p1 - 1]

        return result

    def _generate(self, tournament):
        scores = {}

        for player in tournament.players:
            scores[player.name] = tournament.player_score(player)

        return self._generate_from_scores(tournament, scores)
