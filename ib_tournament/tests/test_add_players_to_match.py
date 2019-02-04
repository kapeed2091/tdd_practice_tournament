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


class TestAddPlayersToMatch(TestCase):

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
        for round_no in range(total_rounds, 0, -1):
            round_matches_count = 2 ** (total_rounds - round_no)
            for count in range(round_matches_count):
                tournament_matches_to_create.append(
                    TournamentMatch(tournament_id=tournament_id,
                                    round_no=round_no))
        TournamentMatch.objects.bulk_create(tournament_matches_to_create)
        return TournamentMatch.objects.all()

    def test_create_match_players(self):
        from ib_tournament.models import TMPlayer
        usernames = ['user1', 'user2', 'user3', 'user4']
        player_ids = [self.create_player(username) for username in usernames]

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_curr_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)
        self.create_tournament_players(tournament_id, player_ids)
        tournament_matches = self.create_tournament_matches(tournament_id, 2)

        pre_tm_players = list(TMPlayer.objects.all())
        pre_tm_players_count = len(pre_tm_players)
        pre_player_ids = [tm_player.player_id for tm_player in pre_tm_players]

        TMPlayer.add_players_to_matches(tournament_id)
        post_tm_players = list(TMPlayer.objects.all())
        post_tm_players_count = len(post_tm_players)
        post_player_ids = [tm_player.player_id for tm_player in post_tm_players]

        self.assertEqual(post_tm_players_count - pre_tm_players_count, 4)
        self.assertEqual(set(post_player_ids) - set(pre_player_ids),
                         set(player_ids))
        created_tm_players = list(set(post_tm_players) - set(pre_tm_players))
        tournament_match_ids = [tm_player.tournament_match_id
                                for tm_player in created_tm_players]

        for tournament_match in tournament_matches:
            if tournament_match.id in tournament_match_ids:
                tm_players_count_per_match = TMPlayer.objects.filter(
                    tournament_match_id=tournament_match.id).count()
                self.assertEqual(tm_players_count_per_match, 2)

    def test_add_players_to_first_round_matches(self):
        from ib_tournament.models import TMPlayer
        usernames = ['user1', 'user2', 'user3', 'user4']
        player_ids = [self.create_player(username) for username in usernames]

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_curr_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)
        self.create_tournament_players(tournament_id, player_ids)
        self.create_tournament_matches(tournament_id, 2)

        TMPlayer.add_players_to_matches(tournament_id)
        tm_players = TMPlayer.objects.all()
        for tm_player in tm_players:
            self.assertEqual(tm_player.tournament_match.round_no, 1)
