from django.test import TestCase


class TestCreateTournament(TestCase):

    def testcase_create_account(self):
        user_id = 1
        total_rounds = 4
        start_datetime = "2019-12-12 13:00:00"
        from tournament.models import Tournament
        Tournament.create_tournament(user_id, total_rounds, start_datetime)

        tournaments = Tournament.objects.all()
        tournament_object = tournaments[0]

        self.assertEqual(tournaments.count(), 1)
        self.assertEqual(tournament_object.user_id, user_id)
        self.assertEqual(tournament_object.total_rounds, total_rounds)
        self.assertEqual(tournament_object.start_datetime, start_datetime)
