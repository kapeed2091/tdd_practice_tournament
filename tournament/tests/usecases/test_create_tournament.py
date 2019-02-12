from unittest import TestCase


class TestCreateTournament(TestCase):
    import datetime
    NO_OF_ROUNDS = 4
    START_DATETIME = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")

    def test_create_tournament(self):
        tournament_data = {
            'tournament_id': 1,
            'no_of_rounds': self.NO_OF_ROUNDS,
            'start_datetime': self.START_DATETIME
        }
        from tournament.usecases import CreateTournamentInteractor
        usecase = CreateTournamentInteractor()
        usecase.setup(no_of_rounds=self.NO_OF_ROUNDS, start_datetime=self.START_DATETIME)
        usecase_response = usecase.execute()
        self.assertEqual(usecase_response, tournament_data)
