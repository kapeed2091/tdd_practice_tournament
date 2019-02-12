import datetime

from unittest import TestCase


class TestSQLStorage(TestCase):

    def test_create_tournament(self):
        tournament_id = 1
        no_of_rounds = 2
        start_datetime = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")

        from tournament.storages.sql_storage import SQLStorage
        sql_storage = SQLStorage()
        create_storage_return_value = sql_storage.create_tournament(
            no_of_rounds=no_of_rounds,
            start_datetime=start_datetime
        )
        self.assertEqual(create_storage_return_value, tournament_id)

    def test_create_two_tournaments(self):
        tournaments = [
            {
                "id": 1,
                "no_of_rounds": 2,
                "start_datetime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")
            },
            {
                "id": 2,
                "no_of_rounds": 2,
                "start_datetime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")
            }
        ]

        from tournament.models import Tournament
        from tournament.storages.sql_storage import SQLStorage
        sql_storage = SQLStorage()

        tournament_id_1 = sql_storage.create_tournament(
            no_of_rounds=tournaments[0]["no_of_rounds"],
            start_datetime=tournaments[0]["start_datetime"]
        )
        tournament_id_2 = sql_storage.create_tournament(
            no_of_rounds=tournaments[1]["no_of_rounds"],
            start_datetime=tournaments[1]["start_datetime"]
        )

        self.assertNotEqual(tournament_id_1, tournament_id_2)
        self.assertEqual(Tournament.objects.all().count(), 2)

        tournaments_from_db = list(Tournament.objects.all().order_by('id').values(
                'id', 'no_of_rounds', 'start_datetime'))
        for tournament in tournaments_from_db:
            tournament['start_datetime'] = datetime.datetime.strptime(tournament['start_datetime'], '%m/%d/%Y, %H:%M:%S')

        self.assertEqual(tournaments_from_db, tournaments)
