from django.test import TestCase


def get_curr_day_datetime_str():
    from ib_common.date_time_utils.get_current_local_date_time import \
        get_current_local_date_time
    from ib_common.date_time_utils.convert_datetime_to_local_string import \
        convert_datetime_to_local_string
    from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT

    curr_day_datetime = get_current_local_date_time()
    return convert_datetime_to_local_string(
        curr_day_datetime, DEFAULT_DATE_TIME_FORMAT)


class TestTournamentWinnerUpdation(TestCase):
    def __init__(self, *args, **kwargs):
        self.player_ids = list()
        self.tournament_id = None
        self.tournament_winner_id = None
        super(TestTournamentWinnerUpdation, self).__init__(*args, **kwargs)

    @staticmethod
    def create_player(username):
        from ib_tournament.models import Player
        player = Player.objects.create(username=username)
        return player.id

    @staticmethod
    def create_tournament(tournament_details):
        from ib_tournament.models import Tournament
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT

        start_datetime = convert_string_to_local_date_time(
            tournament_details['start_datetime'], DEFAULT_DATE_TIME_FORMAT)
        tournament = Tournament.objects.create(
            total_rounds=tournament_details['total_rounds'],
            start_datetime=start_datetime, name=tournament_details['name'])
        return tournament.id

    @staticmethod
    def create_tournament_players(tournament_id, player_ids):
        from ib_tournament.models import TournamentPlayer
        tournament_players_to_create = [
            TournamentPlayer(tournament_id=tournament_id, player_id=player_id)
            for player_id in player_ids]
        TournamentPlayer.objects.bulk_create(tournament_players_to_create)
        return

    @staticmethod
    def create_tournament_matches(tournament_id, total_rounds):
        from ib_tournament.models import TournamentMatch

        tournament_matches_to_create = list()
        for round_no in range(1, total_rounds + 1):
            round_matches_count = 2 ** (total_rounds - round_no)
            for count in range(round_matches_count):
                tournament_matches_to_create.append(
                    TournamentMatch(tournament_id=tournament_id,
                                    round_no=round_no))
        TournamentMatch.objects.bulk_create(tournament_matches_to_create)
        return TournamentMatch.objects.all()

    @staticmethod
    def add_players_to_matches(tournament_matches, player_ids):
        from ib_tournament.models import TMPlayer

        grouped_player_ids = [player_ids[count: count + 2]
                              for count in range(0, len(player_ids), 2)]
        tm_players_to_create = list()
        for index, player_ids_list in enumerate(grouped_player_ids):
            tournament_match = tournament_matches[index]
            for player_id in player_ids_list:
                tm_players_to_create.append(
                    TMPlayer(tournament_match=tournament_match,
                             player_id=player_id))
        TMPlayer.objects.bulk_create(tm_players_to_create)
        return

    def update_winners_in_tournament_matches(self):
        from ib_tournament.models import TMPlayer, TournamentMatch
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from collections import defaultdict

        first_round_t_matches = TournamentMatch.objects.filter(
            tournament_id=self.tournament_id, round_no=1)
        tm_players = TMPlayer.objects.all()

        t_match_id_wise_tm_players = defaultdict(list)
        for tm_player in tm_players:
            t_match_id_wise_tm_players[tm_player.tournament_match_id].append(
                tm_player)

        first_round_winner_ids = list()
        for t_match in first_round_t_matches:
            tm_players = t_match_id_wise_tm_players[t_match.id]
            first_round_winner_ids.append(tm_players[0].player_id)

        last_round_t_match = TournamentMatch.objects.get(
            tournament_id=self.tournament_id, round_no=2)
        second_round_tm_players_to_create = list()
        for winner_id in first_round_winner_ids:
            second_round_tm_players_to_create.append(
                TMPlayer(tournament_match_id=last_round_t_match.id,
                         player_id=winner_id))
        TMPlayer.objects.bulk_create(second_round_tm_players_to_create)
        self.tournament_winner_id = first_round_winner_ids[0]
        last_round_t_match.winner_id = self.tournament_winner_id
        last_round_t_match.save()

        from ib_tournament.constants.general import TMPlayerStatus
        tm_players = TMPlayer.objects.all()
        tm_players.update(status=TMPlayerStatus.COMPLETED.value,
                          completed_datetime=get_current_local_date_time())
        return

    def setUp(self):
        usernames = ['user1', 'user2', 'user3', 'user4']
        self.player_ids = [self.create_player(username)
                           for username in usernames]

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_curr_day_datetime_str(),
            'name': 'Tournament 1'
        }
        self.tournament_id = self.create_tournament(tournament_details)
        self.create_tournament_players(self.tournament_id, self.player_ids)
        tournament_matches = self.create_tournament_matches(
            self.tournament_id, total_rounds=2)
        tournament_matches = tournament_matches.filter(round_no=1)
        self.add_players_to_matches(tournament_matches, self.player_ids)
        self.update_winners_in_tournament_matches()

    def test_update_tournament_winner(self):
        from ib_tournament.models import Tournament

        pre_tournament = Tournament.objects.get(id=self.tournament_id)
        self.assertEqual(pre_tournament.winner_id, None)

        Tournament.update_tournament_winner(
            self.tournament_id, self.tournament_winner_id)
        post_tournament = Tournament.objects.get(id=self.tournament_id)
        self.assertEqual(post_tournament.winner_id, None)
