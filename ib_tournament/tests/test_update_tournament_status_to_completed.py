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


class TestUpdateTournamentStatusToCompleted(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUpdateTournamentStatusToCompleted, self).__init__(
            *args, **kwargs)

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
        return

    def setUp(self):
        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_curr_day_datetime_str(),
            'name': 'Tournament 1'
        }
        self.tournament_id = self.create_tournament(tournament_details)

    def test_update_tournament_status_to_completed(self):
        from ib_tournament.models import Tournament
        from ib_tournament.constants.general import TournamentStatus
        self.update_tournament_status(
            self.tournament_id, TournamentStatus.IN_PROGRESS.value)
        Tournament.update_status_to_completed(self.tournament_id)
        tournament = Tournament.objects.get(id=self.tournament_id)
        self.assertEqual(tournament.status, TournamentStatus.COMPLETED.value)

    def test_pre_tournament_status_is_not_progress(self):
        from ib_tournament.models import Tournament
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            INVALID_TOURNAMENT_STATE

        with self.assertRaisesMessage(BadRequest, INVALID_TOURNAMENT_STATE[0]):
            Tournament.update_status_to_completed(self.tournament_id)
