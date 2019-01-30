from django.test import TestCase


class TestGetTournament(TestCase):
    from datetime import datetime, timedelta

    curr_datetime = datetime.now()
    username = "user1"
    tournaments_data = [
        {
            "id": 1,
            "name": "Knock Out - 1",
            "no_of_rounds": 4,
            "start_date_time": curr_datetime + timedelta(days=1),
            "status": "CAN_JOIN"
        },
        {
            "id": 2,
            "name": "Knock Out - 2",
            "no_of_rounds": 3,
            "start_date_time": curr_datetime + timedelta(days=1),
            "status": "FULL_YET_TO_START"
        },
        {
            "id": 3,
            "name": "Knock Out - 3",
            "no_of_rounds": 3,
            "start_date_time": curr_datetime - timedelta(days=1),
            "status": "IN_PROGRESS"
        },
        {
            "id": 4,
            "name": "Knock Out - 4",
            "no_of_rounds": 5,
            "start_date_time": curr_datetime - timedelta(days=2),
            "status": "COMPLETED"
        },
    ]

    def setUp(self):
        from tournament.models import Tournament

        for tournament in self.tournaments_data:
            Tournament.objects.create(
                name=tournament['name'],
                no_of_rounds=tournament['no_of_rounds'],
                start_date_time=tournament['start_date_time'],
                status=tournament['status'])

    def test_get_all_tournaments(self):
        from tournament.models import Tournament
        tournaments = Tournament.get_all_tournaments()

        self.assertItemsEqual(self.tournaments_data, tournaments)