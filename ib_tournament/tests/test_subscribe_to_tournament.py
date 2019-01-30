from django.test import TestCase


def get_next_day_datetime_str():
    from ib_common.date_time_utils.get_current_local_date_time import \
        get_current_local_date_time
    from ib_common.date_time_utils.convert_datetime_to_local_string import \
        convert_datetime_to_local_string
    from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT
    from datetime import timedelta

    next_day_datetime = get_current_local_date_time() + timedelta(days=1)
    return convert_datetime_to_local_string(
        next_day_datetime, DEFAULT_DATE_TIME_FORMAT)


class TestSubscribeToTournament(TestCase):
    username = 'user1'

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
    def update_tournament_status(tournament_id, status):
        from ib_tournament.models import Tournament
        tournament = Tournament.objects.get(id=tournament_id)
        tournament.status = status
        tournament.save()

    def test_subscribe_to_tournament(self):
        from ib_tournament.models import Tournament, TournamentPlayer

        player_id = self.create_player(self.username)
        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_next_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)
        pre_tournament_players_count = TournamentPlayer.objects.filter(
            tournament_id=tournament_id, player_id=player_id).count()
        Tournament.subscribe_to_tournament(
            tournament_id=tournament_id, player_id=player_id)
        post_tournament_players_count = TournamentPlayer.objects.filter(
            tournament_id=tournament_id, player_id=player_id).count()
        self.assertEqual(
            post_tournament_players_count - pre_tournament_players_count, 1)

    def test_player_can_subscribe_to_can_join_tournaments(self):
        from ib_tournament.models import Tournament
        from ib_tournament.constants.general import TournamentStatus

        player_id = self.create_player(self.username)
        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_next_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)
        self.update_tournament_status(
            tournament_id, TournamentStatus.FULL_YET_TO_START.value)

        from django_swagger_utils.drf_server.exceptions import BadRequest
        with self.assertRaisesMessage(
                BadRequest, "Invalid tournament state"):
            Tournament.subscribe_to_tournament(tournament_id, player_id)

    def test_player_is_invalid(self):
        from ib_tournament.models import Tournament
        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_next_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)

        from django_swagger_utils.drf_server.exceptions import BadRequest
        with self.assertRaisesMessage(
                BadRequest, "Invalid User"):
            Tournament.subscribe_to_tournament(tournament_id, player_id=1525)

    def test_player_can_not_subscribe_twice(self):
        from ib_tournament.models import Tournament

        player_id = self.create_player(self.username)
        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_next_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)
        Tournament.subscribe_to_tournament(
            tournament_id=tournament_id, player_id=player_id)
        from django_swagger_utils.drf_server.exceptions import BadRequest
        with self.assertRaisesMessage(BadRequest, "Can\'t subscribe again"):
            Tournament.subscribe_to_tournament(tournament_id, player_id)

    def test_subscribe_to_invalid_tournament(self):
        from ib_tournament.models import Tournament

        player_id = self.create_player(self.username)
        from django_swagger_utils.drf_server.exceptions import BadRequest
        with self.assertRaisesMessage(BadRequest, "Invalid Tournament"):
            Tournament.subscribe_to_tournament(
                tournament_id=1213, player_id=player_id)

    def test_max_players_subscribed(self):
        from ib_tournament.models import Tournament
        from ib_tournament.constants.general import TournamentStatus

        player_usernames = ['user1', 'user2', 'user3', 'user4']
        player_ids = list()
        for username in player_usernames:
            player_ids.append(self.create_player(username))

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_next_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)
        for player_id in player_ids:
            Tournament.subscribe_to_tournament(tournament_id, player_id)

        tournament = Tournament.objects.get(id=tournament_id)
        self.assertEqual(tournament.status,
                         TournamentStatus.FULL_YET_TO_START.value)
