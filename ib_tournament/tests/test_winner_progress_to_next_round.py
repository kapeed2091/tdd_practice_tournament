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


class TestWinnerProgressToNextRound(TestCase):
    def __init__(self, *args, **kwargs):
        self.player_ids = list()
        self.tournament_id = None
        self.tournament_match_id = None
        self.winner_id = None
        super(TestWinnerProgressToNextRound, self).__init__(*args, **kwargs)

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

    def update_winner_in_tournament_match(self):
        from ib_tournament.models import TMPlayer, TournamentMatch
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        tm_players = TMPlayer.objects.all()
        self.tournament_match_id = tm_players[0].tournament_match_id
        tm_players = tm_players.filter(
            tournament_match_id=self.tournament_match_id)

        from ib_tournament.constants.general import TMPlayerStatus
        tm_players.update(status=TMPlayerStatus.COMPLETED.value,
                          completed_datetime=get_current_local_date_time())
        tournament_match = TournamentMatch.objects.get(
            id=self.tournament_match_id)
        self.winner_id = tm_players[0].player_id
        tournament_match.winner_id = self.winner_id
        tournament_match.save()
        return

    def update_winner_in_final_round_tournament_match(self, final_round_no):
        from ib_tournament.models import TMPlayer, TournamentMatch
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        tm_players = TMPlayer.objects.all()
        self.tournament_match_id = tm_players[0].tournament_match_id
        tm_players = tm_players.filter(
            tournament_match_id=self.tournament_match_id)

        from ib_tournament.constants.general import TMPlayerStatus
        tm_players.update(status=TMPlayerStatus.COMPLETED.value,
                          completed_datetime=get_current_local_date_time())
        tournament_match = TournamentMatch.objects.get(
            id=self.tournament_match_id)
        self.winner_id = tm_players[0].player_id
        tournament_match.winner_id = self.winner_id
        tournament_match.save()

        final_round_t_match = TournamentMatch.objects.get(
            tournament_id=self.tournament_id, round_no=final_round_no)
        TMPlayer.objects.create(
            tournament_match=final_round_t_match, player_id=self.player_ids[0])
        TMPlayer.objects.create(
            tournament_match=final_round_t_match, player_id=self.player_ids[1])
        final_round_t_match.winner_id = self.player_ids[0]
        final_round_t_match.save()
        return final_round_t_match.id, final_round_t_match.winner_id

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
        self.update_winner_in_tournament_match()

    def test_winner_progress_to_next_round(self):
        from ib_tournament.models import TournamentMatch, TMPlayer

        TournamentMatch.promote_winner_to_next_round(
            self.tournament_match_id, self.winner_id)
        round_2_tm_ids = list(TournamentMatch.objects.filter(
            round_no=2).values_list('id', flat=True))
        winner_promoted_to_round_2 = TMPlayer.objects.filter(
            player_id=self.winner_id,
            tournament_match_id__in=round_2_tm_ids).exists()
        self.assertEqual(winner_promoted_to_round_2, True)

    def test_when_last_round_winner_is_updated(self):
        from ib_tournament.models import TournamentMatch, TMPlayer

        final_round_t_match_id, winner_id = \
            self.update_winner_in_final_round_tournament_match(
                final_round_no=2)
        pre_winner_tm_players_count = TMPlayer.objects.filter(
            player_id=winner_id).count()
        TournamentMatch.promote_winner_to_next_round(
            final_round_t_match_id, winner_id)
        post_winner_tm_players_count = TMPlayer.objects.filter(
            player_id=winner_id).count()
        self.assertEqual(
            post_winner_tm_players_count - pre_winner_tm_players_count, 0)

    def test_player_curr_round_updation(self):
        from ib_tournament.models import TournamentMatch, TournamentPlayer

        TournamentMatch.promote_winner_to_next_round(
            self.tournament_match_id, self.winner_id)
        tournament_player = TournamentPlayer.objects.get(
            tournament_id=self.tournament_id, player_id=self.winner_id)
        self.assertEqual(tournament_player.curr_round_no, 2)
