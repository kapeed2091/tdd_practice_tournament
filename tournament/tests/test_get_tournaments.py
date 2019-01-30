import datetime
from django.test import TestCase


class TestGetTournaments(TestCase):

    user_id_1 = "User1"
    user_id_2 = "User2"

    tournaments = [
        {
            "id": get_uuid(),
            "created_user_id": user_id_1,
            "name": "Tournament1",
            "no_of_rounds": 2,
            "start_datetime": datetime.datetime.now() + datetime.timedelta(days=1),
            "status": TournamentStatus.YET_TO_START.value
        },
        {
            "id": get_uuid(),
            "created_user_id": user_id_2,
            "name": "Tournament2",
            "no_of_rounds": 3,
            "start_datetime": datetime.datetime.now() - datetime.timedelta(days=1),
            "status": TournamentStatus.IN_PROGRESS.value
        }
    ]

    def setUp(self):
        from tournament.models import KoTournament

        tournament_objs_to_create = [
            KoTournament(
                id=each['id'],
                created_user_id=each['created_user_id'],
                name=each['name'],
                no_of_rounds=each['no_of_rounds'],
                start_datetime=each['start_datetime'],
                status=each['status']
            ) for each in self.tournaments
        ]
        KoTournament.objects.bulk_create(tournament_objs_to_create)

    def test_get_all_tournaments(self):
        from tournament.models import KoTournament
        import copy

        tournaments_expected = copy.deepcopy(self.tournaments)
        for each in tournaments_expected:
            each.pop('created_user_id')

        tournaments = KoTournament.get_all_tournaments()
        self.assertItemsEqual(tournaments_expected, tournaments)
