from django.test import TestCase
from tournament.models import Tournament


class TestGetAllTournaments(TestCase):

    def test_case_get_all_tournaments(self):
        tournaments = [
            {
                "name": "tournament_1",
                "total_rounds": 2,
                "start_datetime": "",
                "status": "CAN_JOIN"
            },
            {
                "name": "tournament_2",
                "total_rounds": 3,
                "start_datetime": "",
                "status": "FULL_YET_TO_START"
            },
            {
                "name": "tournament_3",
                "total_rounds": 4,
                "start_datetime": "",
                "status": "IN_PROGRESS"
            },
            {
                "name": "tournament_4",
                "total_rounds": 5,
                "start_datetime": "",
                "status": "COMPLETED"
            }
        ]

        for each in tournaments:
            Tournament.objects.create(
                name=each["name"],
                total_rounds=each["total_rounds"],
                start_datetime=each["start_datetime"],
                status=each["status"]
            )

        tournament_details = Tournament.get_all_tournament_details()

        tournaments_sorted = \
            sorted(tournaments, key=lambda k: k['start_datetime'])

        tournaments_sorted_set = set(tournaments_sorted.items())
        tournament_details_set = set(tournament_details.items())

        self.assertTrue(
            tournaments_sorted_set.issubset(tournament_details_set))
