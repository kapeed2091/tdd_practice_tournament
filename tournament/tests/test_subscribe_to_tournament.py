from django.test import TestCase


class TestSubscribeToTournament(TestCase):

    def testcase_subscribe_to_tournament(self):
        from tournament.models import UserTournament

        user_id = 1
        tournament_id = 1
        UserTournament.subscribe_to_tournament(user_id, tournament_id)
        user_tournaments = UserTournament.objects.all()
        user_tournament = user_tournaments[0]

        self.assertEqual(user_tournaments.count(), 1)
        self.assertEqual(user_tournament.user_id, user_id)
        self.assertEqual(user_tournament.tournament_id, tournament_id)
