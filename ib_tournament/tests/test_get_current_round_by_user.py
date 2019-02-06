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


class TestGetCurrentRoundByUser(TestCase):
    username_wise_user_data = {
        'user1': {
            'name': 'User 1',
            'age': 22,
            'gender': 'MALE'
        },
        'user2': {
            'name': 'User 2',
            'age': 23,
            'gender': 'MALE'
        },
        'user3': {
            'name': 'User 3',
            'age': 24,
            'gender': 'FEMALE'
        },
        'user4': {
            'name': 'User 4',
            'age': 25,
            'gender': 'MALE'
        },
        'user5': {
            'name': 'User 5',
            'age': 25,
            'gender': 'MALE'
        }
    }

    def __init__(self, *args, **kwargs):
        self.player_ids = list()
        self.tournament_id = None
        self.tournament_match_id = None
        self.winner_id = None
        super(TestGetCurrentRoundByUser, self).__init__(*args, **kwargs)

    def create_player(self, username):
        from ib_tournament.models import Player
        user_dict = self.username_wise_user_data[username]
        player = Player.objects.create(
            username=username, name=user_dict['name'], age=user_dict['age'],
            gender=user_dict['gender'])
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
            TournamentPlayer(tournament_id=tournament_id, player_id=player_id,
                             curr_round_no=1)
            for player_id in player_ids]
        TournamentPlayer.objects.bulk_create(tournament_players_to_create)
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

    def test_get_current_round_by_user(self):
        from ib_tournament.models import TournamentPlayer
        player_id = self.player_ids[0]
        t_player = TournamentPlayer.objects.get(
            tournament_id=self.tournament_id, player_id=player_id)
        t_player.curr_round_no = 2
        t_player.save()

        current_round = TournamentPlayer.get_player_current_round(
            tournament_id=self.tournament_id, player_id=player_id)
        self.assertEqual(current_round, 2)

    def test_when_user_is_not_in_tournament(self):
        from ib_tournament.models import TournamentPlayer
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            PLAYER_NOT_IN_TOURNAMENT
        player_id = self.create_player('user5')
        # TODO: DOUBT: How to get to red state here?
        with self.assertRaisesMessage(BadRequest, PLAYER_NOT_IN_TOURNAMENT[0]):
            TournamentPlayer.get_player_current_round(
                tournament_id=self.tournament_id, player_id=player_id)
