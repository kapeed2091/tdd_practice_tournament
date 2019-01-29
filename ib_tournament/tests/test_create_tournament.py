from django.test import TestCase


class TestCreateTournament(TestCase):

    def test_create_tournament(self):
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from ib_common.date_time_utils.convert_datetime_to_local_string import \
            convert_datetime_to_local_string
        from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT

        start_datetime = convert_datetime_to_local_string(
            get_current_local_date_time(), DEFAULT_DATE_TIME_FORMAT)
        total_rounds = 3

        from ib_tournament.models import Tournament
        initial_tournaments_count = Tournament.objects.count()
        Tournament.create_tournament(total_rounds, start_datetime)
        tournaments_count = Tournament.objects.count()

        self.assertEqual(tournaments_count - initial_tournaments_count, 1)

    def test_invalid_datetime(self):
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from ib_common.date_time_utils.convert_datetime_to_local_string import \
            convert_datetime_to_local_string
        from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT

        start_datetime = convert_datetime_to_local_string(
            get_current_local_date_time(), DEFAULT_DATE_TIME_FORMAT)
        total_rounds = 3

        from ib_tournament.models import Tournament
        from django_swagger_utils.drf_server.exceptions import BadRequest
        with self.assertRaisesMessage(BadRequest, "Invalid Datetime"):
            Tournament.create_tournament(total_rounds, start_datetime)