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


class TestGetWinnerProfileOfTournament(TestCase):
    username_wise_user_data = {
        'user1': {
            'name': 'User 1',
            'age': 22,
            'gender': 'MALE'
        }
    }

    def __init__(self, *args, **kwargs):
        self.player_id = None
        self.tournament_id = None
        super(TestGetWinnerProfileOfTournament, self).__init__(*args, **kwargs)

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
    def update_tournament_winner(tournament_id, winner_id):
        from ib_tournament.models import Tournament
        tournament = Tournament.objects.get(id=tournament_id)
        tournament.winner_id = winner_id
        tournament.save()
        return

    def setUp(self):
        self.player_id = self.create_player('user1')
        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_curr_day_datetime_str(),
            'name': 'Tournament 1'
        }
        self.tournament_id = self.create_tournament(tournament_details)

    def test_get_winner_profile_of_tournament(self):
        from ib_tournament.models import Tournament
        self.update_tournament_winner(self.tournament_id, self.player_id)
        winner_profile = Tournament.get_winner_profile(self.tournament_id)
        expected_profile = self.username_wise_user_data['user1']
        self.assertEqual(expected_profile, winner_profile)
