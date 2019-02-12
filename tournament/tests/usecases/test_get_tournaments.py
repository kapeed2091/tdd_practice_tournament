from unittest import TestCase

class TestGetTournaments(TestCase):

    def test_get_tournaments(self):
        import datetime
        tournaments = [
            {
                'tournament_id': 1,
                'no_of_rounds': 4,
                'start_datetime': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")
            }
        ]

        from tournament.usecases import GetTournamentsInteractor
        usecase = GetTournamentsInteractor()
        usecase_response = usecase.execute()
        self.assertEqual(usecase_response, tournaments)
