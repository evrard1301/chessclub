from datetime import date
from model.datastore import DataStore
from model.match import MatchResult
from model.pairgenerator import SwissPairGenerator
from model.player import Player
from model.round import Round
from model.tournament import Tournament


def setup():
    tournament = Tournament('THE tournament',
                            'ChessClub building',
                            date(2020, 3, 7),
                            date(2020, 3, 7),
                            'blitz',
                            'my first tournament')

    tournament.add_round(Round('Round 1',
                               date(2020, 3, 8),
                               date(2020, 3, 9)))
    tournament.add_round(Round('Round 2',
                               date(2020, 3, 9),
                               date(2020, 3, 10)))
    tournament.add_round(Round('Round 3',
                               date(2020, 3, 10),
                               date(2020, 3, 11)))

    datastore = DataStore()
    tournament.add_player(Player('Kazparov', 'Garry', '12/08/1995', 'M', '1'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Carlsen', 'Magnus', '12/08/1995', 'M', '2'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Fischer', 'Bobby', '12/08/1995', 'M', '3'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Capablanca',
                                 'Jose Raul', '12/08/1995', 'M', '4'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Karpov', 'Anatoly', '12/08/1995', 'M', '5'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Botvinnik',
                                 'Mikhail', '12/08/1995', 'M', '6'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Kramnik',
                                 'Vladimir', '12/08/1995', 'M', '7'))
    datastore.store_player(tournament._players[-1])
    tournament.add_player(Player('Lasker', 'Emanuel', '12/08/1995', 'M', '8'))
    datastore.store_player(tournament._players[-1])

    return tournament, datastore


def check_result(oracle, result):
    assert len(oracle) == len(result)

    for i in range(0, len(oracle)):
        assert oracle[i][0].ranking == result[i][0].ranking
        assert oracle[i][1].ranking == result[i][1].ranking


def make_pairs(datastore, *args):
    result = []
    for i in range(0, len(args)):
        result.append((
            datastore.find_players_by_ranking(args[i][0])[0],
            datastore.find_players_by_ranking(args[i][1])[0]
        ))

    return result


def test_first_round():
    gen = SwissPairGenerator()
    tournament, datastore = setup()
    result = gen.generate(tournament)

    oracle = make_pairs(datastore, (1, 5), (2, 6), (3, 7), (4, 8))

    check_result(oracle, result)


def test_second_round():
    gen = SwissPairGenerator()
    tournament, datastore = setup()

    initial = gen.generate(tournament)
    tournament.play_round(initial, [MatchResult.WON,
                                    MatchResult.LOSE,
                                    MatchResult.DRAW,
                                    MatchResult.LOSE])
    # Points
    # 1-> 1
    # 2-> 0
    # 3-> 0.5
    # 4-> 0
    # 5-> 0
    # 6-> 1
    # 7-> 0.5
    # 8-> 1

    # Order
    # 1 6 8 3 7 2 4 5

    oracle = make_pairs(datastore, (1, 6), (8, 3), (7, 2), (4, 5))
    result = gen.generate(tournament)
    check_result(oracle, result)


def test_first_players_have_already_played_together():
    gen = SwissPairGenerator()
    tournament, datastore = setup()

    initial = gen.generate(tournament)
    tournament.play_round(initial, [MatchResult.WON,
                                    MatchResult.LOSE,
                                    MatchResult.DRAW,
                                    MatchResult.LOSE])

    def mock_score(player):
        if int(player.ranking) == 1 \
           or int(player.ranking) == 5:
            return 1
        return 0

    tournament.player_score = mock_score

    tournament.play_round(initial, [MatchResult.DRAW,
                                    MatchResult.DRAW,
                                    MatchResult.DRAW,
                                    MatchResult.DRAW])
    # order: 1 5 2 3 4 6 7 8
    oracle = make_pairs(datastore, (1, 2), (5, 3), (4, 6), (7, 8))
    result = gen.generate(tournament)
    check_result(oracle, result)


def test_first_player_have_already_played_against_snd_and_third():
    gen = SwissPairGenerator()
    tournament, datastore = setup()

    tournament.play_round([
        (tournament.players[0], tournament.players[1]),
        (tournament.players[2], tournament.players[3]),
        (tournament.players[4], tournament.players[5]),
        (tournament.players[6], tournament.players[7])
    ],
                          [MatchResult.DRAW,
                           MatchResult.DRAW,
                           MatchResult.DRAW,
                           MatchResult.DRAW])

    tournament.play_round([
        (tournament.players[0], tournament.players[2]),
        (tournament.players[3], tournament.players[4]),
        (tournament.players[5], tournament.players[6]),
        (tournament.players[7], tournament.players[1])
    ],
                          [MatchResult.DRAW,
                           MatchResult.DRAW,
                           MatchResult.DRAW,
                           MatchResult.DRAW])
    for i, player in enumerate(tournament.players):
        player.ranking = i + 1

    def mock_player_score(player):
        return 0

    tournament.player_score = mock_player_score
    initial = gen.generate(tournament)

    assert initial[0][0].name == tournament.players[0].name
    assert initial[0][1].name == tournament.players[3].name
