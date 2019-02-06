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


class TestGetOpponentProfileInRound(TestCase):
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
        }
    }

    def __init__(self, *args, **kwargs):
        self.player_ids = list()
        self.tournament_id = None
        self.tournament_match_id = None
        self.match_player_ids = []
        super(TestGetOpponentProfileInRound, self).__init__(*args, **kwargs)

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

    def setUp(self):
        usernames = self.username_wise_user_data.keys()
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

    def test_get_opponent_profile_of_round(self):
        from ib_tournament.models import TMPlayer, TournamentMatch, Player

        first_round_t_matches = TournamentMatch.objects.filter(
            tournament_id=self.tournament_id, round_no=1)
        t_match_id = first_round_t_matches[0].id
        tm_players = TMPlayer.objects.filter(tournament_match_id=t_match_id)
        player_ids = [tm_player.player_id for tm_player in tm_players]

        req_player_id = player_ids[0]
        opponent_player_id = player_ids[1]
        opponent_player = Player.objects.get(id=opponent_player_id)
        expected_profile = self.username_wise_user_data[
            opponent_player.username]

        opponent_profile = TMPlayer.get_opponent_profile(
            self.tournament_id, req_player_id, round_no=1)

        self.assertEqual(expected_profile, opponent_profile)
