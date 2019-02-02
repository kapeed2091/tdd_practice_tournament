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


def get_curr_day_datetime_str():
    from ib_common.date_time_utils.get_current_local_date_time import \
        get_current_local_date_time
    from ib_common.date_time_utils.convert_datetime_to_local_string import \
        convert_datetime_to_local_string
    from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT

    curr_day_datetime = get_current_local_date_time()
    return convert_datetime_to_local_string(
        curr_day_datetime, DEFAULT_DATE_TIME_FORMAT)


class TestStartTournament(TestCase):
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

    def test_start_tournament(self):
        from ib_tournament.models import Tournament
        from ib_tournament.constants.general import TournamentStatus

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_curr_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)
        self.update_tournament_status(
            tournament_id, TournamentStatus.FULL_YET_TO_START.value)
        Tournament.start_tournament(tournament_id)

        tournament = Tournament.objects.get(id=tournament_id)
        self.assertEqual(tournament.status, TournamentStatus.IN_PROGRESS.value)

    def test_start_datetime_not_reached(self):
        from ib_tournament.models import Tournament

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_next_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)

        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            START_DATE_NOT_REACHED
        with self.assertRaisesMessage(BadRequest, START_DATE_NOT_REACHED[0]):
            Tournament.start_tournament(tournament_id)

    def test_tournament_status_is_full_yet_to_start(self):
        from ib_tournament.models import Tournament

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_curr_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)

        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            TOURNAMENT_STATUS_IS_NOT_FULL_YET_TO_START
        with self.assertRaisesMessage(
                BadRequest, TOURNAMENT_STATUS_IS_NOT_FULL_YET_TO_START[0]):
            Tournament.start_tournament(tournament_id)
