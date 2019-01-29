from django.test import TestCase
import datetime


class TestCreateTournament(TestCase):
    user_id = 'User'

    def test_create_tournament(self):
        from tournament.models import Tournament
        now = datetime.datetime.now()
        start_datetime = now + datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.user_id,
            "no_of_rounds": 3,
            "start_datetime": start_datetime
        }
        tournament_response = Tournament.create_tournament(**tournament_request)
        self.assertEqual(tournament_request, tournament_response)
