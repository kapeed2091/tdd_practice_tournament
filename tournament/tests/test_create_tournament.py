from django.test import TestCase
from freezegun import freeze_time
import datetime

from django_swagger_utils.drf_server.exceptions import BadRequest


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

    def test_create_tournament_with_negative_no_of_rounds(self):
        from tournament.models import Tournament
        now = datetime.datetime.now()
        start_datetime = now + datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.user_id,
            "no_of_rounds": -1,
            "start_datetime": start_datetime
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid number of rounds'):
            Tournament.create_tournament(**tournament_request)

    def test_create_tournament_with_zero_no_of_rounds(self):
        from tournament.models import Tournament
        now = datetime.datetime.now()
        start_datetime = now + datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.user_id,
            "no_of_rounds": 0,
            "start_datetime": start_datetime
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid number of rounds'):
            Tournament.create_tournament(**tournament_request)

    def test_create_tournament_with_start_datetime_less_than_now(self):
        from tournament.models import Tournament
        now = datetime.datetime.now()
        start_datetime = now - datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.user_id,
            "no_of_rounds": 3,
            "start_datetime": start_datetime
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid start_datetime'):
            Tournament.create_tournament(**tournament_request)

    @freeze_time('12-09-2018 12:12:12')
    def test_create_tournament_with_start_datetime_equals_now(self):
        from tournament.models import Tournament
        now = datetime.datetime.now()
        tournament_request = {
            "created_user_id": self.user_id,
            "no_of_rounds": 3,
            "start_datetime": now
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid start_datetime'):
            Tournament.create_tournament(**tournament_request)
