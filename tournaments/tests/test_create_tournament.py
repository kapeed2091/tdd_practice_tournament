from django.test import TestCase
from ib_common.date_time_utils.convert_string_to_local_date_time \
    import convert_string_to_local_date_time


class TestCreateTournament(TestCase):
    user_id = 1
    total_rounds = 4
    start_datetime = "2019-12-12 13:00:00"
    user_name = "John"
    user = None
    tournament = None
    date_time_format = '%Y-%m-%d %H:%M:%S'
    start_datetime_obj = convert_string_to_local_date_time(
        start_datetime, date_time_format
    )

    def test_case_create_tournament(self):
        self.create_user()

        from tournaments.models import Tournament
        Tournament.create_tournament(
            user_id=self.user.id, total_rounds=self.total_rounds,
            start_datetime=self.start_datetime_obj
        )

        obj_exists = Tournament.objects.filter(
            user_id=self.user.id, total_rounds=self.total_rounds,
            start_datetime=self.start_datetime_obj
        ).exists()

        self.assertTrue(obj_exists)
        self.assertEqual(Tournament.objects.all().count(), 1)

    def test_case_invalid_user_id(self):
        from tournaments.models import Tournament

        from tournaments.exceptions.custom_exceptions import InvalidUserId
        with self.assertRaises(InvalidUserId):
            Tournament.create_tournament(
                user_id=self.user_id, total_rounds=self.total_rounds,
                start_datetime=self.start_datetime_obj
            )

    def test_case_invalid_start_date(self):
        start_datetime = "2017-12-12 13:00:00"

        start_datetime_obj = convert_string_to_local_date_time(
            start_datetime, self.date_time_format
        )

        self.create_user()

        from tournaments.models import Tournament

        from tournaments.exceptions.custom_exceptions import InvalidStartDateTime
        with self.assertRaises(InvalidStartDateTime):
            Tournament.create_tournament(
                user_id=self.user_id, total_rounds=self.total_rounds,
                start_datetime=start_datetime_obj
            )

    def test_case_invalid_total_rounds(self):
        self.create_user()
        self.total_rounds = -4

        from tournaments.models import Tournament

        from tournaments.exceptions.custom_exceptions import InvalidTotalRounds
        with self.assertRaises(InvalidTotalRounds):
            Tournament.create_tournament(
                user_id=self.user_id, total_rounds=self.total_rounds,
                start_datetime=self.start_datetime_obj
            )

    def create_user(self):
        from tournaments.models import User
        user = User.objects.create(
            name=self.user_name,
            age=14,
            gender="MALE"
        )
        self.user = user
