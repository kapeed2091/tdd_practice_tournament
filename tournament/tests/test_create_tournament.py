from django.test import TestCase


class TestCreateTournament(TestCase):

    def testcase_create_account(self):
        user_id = 1
        total_rounds = 4
        start_datetime = "2019-12-12 13:00:00"
        user_name = "John"

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        date_time_format = '%Y-%m-%d %H:%M:%S'

        start_datetime = convert_string_to_local_date_time(
            start_datetime, date_time_format
        )
        from tournament.models import User
        User.objects.create(name=user_name)
        from tournament.models import Tournament
        Tournament.create_tournament(user_id, total_rounds, start_datetime)

        tournaments = Tournament.objects.all()
        tournament_object = tournaments[0]

        self.assertEqual(tournaments.count(), 1)
        self.assertEqual(tournament_object.user_id, user_id)
        self.assertEqual(tournament_object.total_rounds, total_rounds)
        self.assertEqual(tournament_object.start_datetime, start_datetime)

    def testcase_invalid_user_id(self):
        user_id = 1
        total_rounds = 4
        start_datetime = "2019-12-12 13:00:00"

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        date_time_format = '%Y-%m-%d %H:%M:%S'

        start_datetime = convert_string_to_local_date_time(
            start_datetime, date_time_format
        )
        from tournament.models import Tournament

        from tournament.exceptions.exceptions import InvalidUserId
        with self.assertRaises(InvalidUserId):
            Tournament.create_tournament(user_id, total_rounds, start_datetime)

    def test_case_invalid_start_date(self):
        user_id = 1
        total_rounds = 4
        start_datetime = "2017-12-12 13:00:00"
        user_name = "John"

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        date_time_format = '%Y-%m-%d %H:%M:%S'

        start_datetime = convert_string_to_local_date_time(
            start_datetime, date_time_format
        )

        from tournament.models import User
        User.objects.create(name=user_name)

        from tournament.models import Tournament

        from tournament.exceptions.exceptions import InvalidStartDateTime
        with self.assertRaises(InvalidStartDateTime):
            Tournament.create_tournament(user_id, total_rounds, start_datetime)

    def test_case_invalid_total_rounds(self):
        user_id = 1
        total_rounds = -4
        start_datetime = "2019-12-12 13:00:00"
        user_name = "John"

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        date_time_format = '%Y-%m-%d %H:%M:%S'

        start_datetime = convert_string_to_local_date_time(
            start_datetime, date_time_format
        )

        from tournament.models import User
        User.objects.create(name=user_name)

        from tournament.models import Tournament

        from tournament.exceptions.exceptions import InvalidTotalRounds
        with self.assertRaises(InvalidTotalRounds):
            Tournament.create_tournament(user_id, total_rounds, start_datetime)
