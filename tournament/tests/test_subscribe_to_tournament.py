from django.test import TestCase


class TestSubscribeToTournament(TestCase):

    def testcase_subscribe_to_tournament(self):
        from tournament.models import User, Tournament, UserTournament
        total_rounds = 4
        start_datetime = "2019-12-12 13:00:00"
        user_name = "John"

        user = User.objects.create(name=user_name)

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        date_time_format = '%Y-%m-%d %H:%M:%S'

        start_datetime = convert_string_to_local_date_time(
            start_datetime, date_time_format
        )
        tournament = Tournament.objects.create(
            user_id=user.id,
            total_rounds=total_rounds,
            start_datetime=start_datetime
        )
        UserTournament.subscribe_to_tournament(user.id, tournament.id)
        user_tournaments = UserTournament.objects.all()
        user_tournament = user_tournaments[0]

        self.assertEqual(user_tournaments.count(), 1)
        self.assertEqual(user_tournament.user_id, user.id)
        self.assertEqual(user_tournament.tournament_id, tournament.id)

    def test_case_invalid_tournament_id(self):
        from tournament.models import User, UserTournament
        user_name = "John"

        user = User.objects.create(name=user_name)

        tournament_id = 1

        from tournament.exceptions.exceptions import InvalidTournamentId
        with self.assertRaises(InvalidTournamentId):
            UserTournament.subscribe_to_tournament(user.id, tournament_id)

    def test_case_invalid_user_id(self):
        from tournament.models import Tournament, UserTournament

        user_id = 1
        total_rounds = 4
        start_datetime = "2019-12-12 13:00:00"

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        date_time_format = '%Y-%m-%d %H:%M:%S'

        start_datetime = convert_string_to_local_date_time(
            start_datetime, date_time_format
        )
        tournament = Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime
        )

        from tournament.exceptions.exceptions import InvalidUserId
        with self.assertRaises(InvalidUserId):
            UserTournament.subscribe_to_tournament(user_id, tournament.id)
