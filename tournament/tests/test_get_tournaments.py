import datetime
from django.test import TestCase

from tournament.constants.general import TournamentStatus
from tournament.utils.date_time_utils import get_current_date_time


class TestGetTournaments(TestCase):

    user_id_1 = "User1"
    user_id_2 = "User2"

    tournaments = [
        {
            "created_user_id": user_id_1,
            "name": "Tournament1",
            "no_of_rounds": 2,
            "start_datetime": get_current_date_time() + datetime.timedelta(days=1),
            "status": TournamentStatus.YET_TO_START.value
        },
        {
            "created_user_id": user_id_2,
            "name": "Tournament2",
            "no_of_rounds": 3,
            "start_datetime": get_current_date_time() - datetime.timedelta(days=1),
            "status": TournamentStatus.IN_PROGRESS.value
        }
    ]

    def setUp(self):
        from tournament.models import KoTournament
        for each in self.tournaments:
            KoTournament.objects.create(**each)

    def test_get_all_tournaments(self):
        from tournament.models import KoTournament
        import copy

        tournaments_expected = copy.deepcopy(self.tournaments)

        id_index = 1
        for each in tournaments_expected:
            each.pop('created_user_id')
            each['id'] = id_index
            id_index += 1

        tournaments = KoTournament.get_all_tournaments()
        self.assertItemsEqual(tournaments_expected, tournaments)
