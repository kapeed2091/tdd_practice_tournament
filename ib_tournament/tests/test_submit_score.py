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


class TestSubmitScore(TestCase):
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
        super(TestSubmitScore, self).__init__(*args, **kwargs)

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
    def create_tournament_matches(tournament_id, matches_count):
        from ib_tournament.models import TournamentMatch
        tournament_matches_to_create = [
            TournamentMatch(tournament_id=tournament_id, round_no=1)
            for count in range(matches_count)]
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
            self.tournament_id, 3)
        self.add_players_to_matches(tournament_matches, self.player_ids)

    def test_submit_score(self):
        from ib_tournament.models import TMPlayer
        from ib_tournament.constants.general import TMPlayerStatus
        tm_players = TMPlayer.objects.all()
        tm_player = tm_players[0]
        tm_player_id = tm_player.id
        player_id = tm_players[0].player_id
        tournament_match_id = tm_players[0].tournament_match_id
        score = 50
        tm_player.status = TMPlayerStatus.IN_PROGRESS.value
        tm_player.save()

        TMPlayer.submit_score(player_id, tournament_match_id, score)
        tm_player = TMPlayer.objects.get(id=tm_player_id)
        self.assertEqual(tm_player.score, score)

    def test_status_changes_to_completed(self):
        from ib_tournament.models import TMPlayer
        from ib_tournament.constants.general import TournamentStatus
        from ib_tournament.constants.general import TMPlayerStatus
        tm_players = TMPlayer.objects.all()
        tm_player = tm_players[0]
        tm_player_id = tm_player.id
        player_id = tm_players[0].player_id
        tournament_match_id = tm_players[0].tournament_match_id
        score = 50
        tm_player.status = TMPlayerStatus.IN_PROGRESS.value
        tm_player.save()

        TMPlayer.submit_score(player_id, tournament_match_id, score)
        tm_player = TMPlayer.objects.get(id=tm_player_id)
        self.assertEqual(tm_player.status, TournamentStatus.COMPLETED.value)

    def test_submit_only_when_status_is_in_progress(self):
        from ib_tournament.models import TMPlayer
        from ib_tournament.constants.general import TournamentStatus
        tm_players = TMPlayer.objects.all()
        tm_player = tm_players[0]
        player_id = tm_players[0].player_id
        tournament_match_id = tm_players[0].tournament_match_id
        score = 50
        tm_player.status = TournamentStatus.COMPLETED.value
        tm_player.save()

        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            SUBMIT_WHEN_STATUS_IS_IN_PROGRESS
        with self.assertRaisesMessage(
                BadRequest, SUBMIT_WHEN_STATUS_IS_IN_PROGRESS[0]):
            TMPlayer.submit_score(player_id, tournament_match_id, score)

    def test_player_not_in_match(self):
        from ib_tournament.models import TMPlayer
        from ib_tournament.constants.general import TournamentStatus
        tm_players = TMPlayer.objects.all()
        tm_player = tm_players[0]
        tournament_match_id = tm_players[0].tournament_match_id
        score = 50
        tm_player.status = TournamentStatus.IN_PROGRESS.value
        tm_player.save()
        player_id = self.create_player('user5')

        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            PLAYER_NOT_IN_MATCH
        with self.assertRaisesMessage(
                BadRequest, PLAYER_NOT_IN_MATCH[0]):
            TMPlayer.submit_score(player_id, tournament_match_id, score)

    def test_winner_declaration(self):
        from ib_tournament.models import TMPlayer, TournamentMatch
        from ib_tournament.constants.general import TournamentStatus
        all_tm_players = TMPlayer.objects.all()
        tournament_match_id = all_tm_players[0].tournament_match_id
        tm_players = TMPlayer.objects.filter(
            tournament_match_id=tournament_match_id)
        tm_players.update(status=TournamentStatus.IN_PROGRESS.value)

        player_ids = [tm_player.player_id for tm_player in tm_players]
        TMPlayer.submit_score(player_ids[0], tournament_match_id, 100)
        TMPlayer.submit_score(player_ids[1], tournament_match_id, 90)

        tournament_match = TournamentMatch.objects.get(id=tournament_match_id)
        self.assertEqual(tournament_match.winner_id, player_ids[0])

    def test_players_scores_are_same(self):
        from ib_tournament.models import TMPlayer, TournamentMatch
        from ib_tournament.constants.general import TournamentStatus
        all_tm_players = TMPlayer.objects.all()
        tournament_match_id = all_tm_players[0].tournament_match_id
        tm_players = TMPlayer.objects.filter(
            tournament_match_id=tournament_match_id)
        tm_players.update(status=TournamentStatus.IN_PROGRESS.value)

        player_ids = [tm_player.player_id for tm_player in tm_players]
        TMPlayer.submit_score(player_ids[0], tournament_match_id, 100)
        TMPlayer.submit_score(player_ids[1], tournament_match_id, 100)

        tm_players = TMPlayer.objects.filter(
            tournament_match_id=tournament_match_id)
        self.assertEqual(tm_players[0].completed_datetime <
                         tm_players[1].completed_datetime, True)

        tournament_match = TournamentMatch.objects.get(id=tournament_match_id)
        self.assertEqual(tournament_match.winner_id, player_ids[0])
