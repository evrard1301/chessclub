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
        players = copy.deepcopy(tournament.players)
        result = []

        players.sort(key=lambda p: int(p.ranking))

        i = 0
        total = int(len(players)/2)

        while i < total:
            result.append((players[i], players[total + i]))
            i += 1

        return result

    def _generate(self, tournament):
        players = copy.deepcopy(tournament.players)
        result = []

        players.sort(reverse=True, key=lambda p: tournament.player_score(p))
        first = True

        while len(players) > 0:
            p0 = 0
            p1 = 1

            if first is True:
                first = False
                my_round = tournament.previous_round()
                matches = my_round.find_matches_by_players(players[p0],
                                                           players[p1])
                if len(matches) > 0:
                    p1 += 1

            result.append((players[p0], players[p1]))

            del players[p0]
            del players[p1 - 1]

        return result
