from django.test import TestCase
from freezegun import freeze_time
import datetime
import copy

from django_swagger_utils.drf_server.exceptions import BadRequest

from tournament.constants.general import TournamentStatus


class TestCreateTournament(TestCase):
    user_id = 'User'
    invalid_user_id = 'Invalid_User'

    def setUp(self):
        from tournament.models import User
        User.objects.create(user_id=self.user_id)

    def test_create_tournament(self):
        from tournament.models import KoTournament
        now = get_current_date_time()
        start_datetime = now + datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.user_id,
            "name": "Tournament1",
            "no_of_rounds": 3,
            "start_datetime": start_datetime
        }
        tournament_response = KoTournament.create_tournament(**tournament_request)
        tournament_response_expected = copy.deepcopy(tournament_request)
        tournament_response_expected['status'] = TournamentStatus.YET_TO_START.value

        self.assertEqual(tournament_response_expected, tournament_response)

    def test_create_tournament_with_negative_no_of_rounds(self):
        from tournament.models import KoTournament
        now = datetime.datetime.now()
        start_datetime = now + datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.user_id,
            "name": "Tournament",
            "no_of_rounds": -1,
            "start_datetime": start_datetime
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid number of rounds'):
            KoTournament.create_tournament(**tournament_request)

    def test_create_tournament_with_zero_no_of_rounds(self):
        from tournament.models import KoTournament
        now = datetime.datetime.now()
        start_datetime = now + datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.user_id,
            "name": "Tournament",
            "no_of_rounds": 0,
            "start_datetime": start_datetime
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid number of rounds'):
            KoTournament.create_tournament(**tournament_request)

    def test_create_tournament_with_start_datetime_less_than_now(self):
        from tournament.models import KoTournament
        now = datetime.datetime.now()
        start_datetime = now - datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.user_id,
            "name": "Tournament",
            "no_of_rounds": 3,
            "start_datetime": start_datetime
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid start_datetime'):
            KoTournament.create_tournament(**tournament_request)

    @freeze_time('12-09-2018 12:12:12')
    def test_create_tournament_with_start_datetime_equals_now(self):
        from tournament.models import KoTournament
        now = datetime.datetime.now()
        tournament_request = {
            "created_user_id": self.user_id,
            "name": "Tournament",
            "no_of_rounds": 3,
            "start_datetime": now
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid start_datetime'):
            KoTournament.create_tournament(**tournament_request)

    def test_create_tournament_with_wrong_user_id(self):
        from tournament.models import KoTournament
        now = datetime.datetime.now()
        start_datetime = now + datetime.timedelta(days=1)
        tournament_request = {
            "created_user_id": self.invalid_user_id,
            "name": "Tournament",
            "no_of_rounds": 3,
            "start_datetime": start_datetime
        }

        with self.assertRaisesMessage(BadRequest, 'Invalid user_id'):
            KoTournament.create_tournament(**tournament_request)
