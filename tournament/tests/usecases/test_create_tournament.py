from unittest import TestCase


class TestCreateTournament(TestCase):
    import datetime
    NO_OF_ROUNDS = 4
    START_DATETIME = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def test_create_tournament(self):
        from tournament.usecases.interactors import CreateTournamentInteractor
        create_tournament_interactor = CreateTournamentInteractor()
        create_tournament_interactor.setup(no_of_rounds=self.NO_OF_ROUNDS,
                                        start_datetime=self.START_DATETIME)
        tournament = create_tournament_interactor.execute()
        self.assertEquals(tournament['no_of_rounds'], self.NO_OF_ROUNDS, 'No of rounds did not match')
        self.assertEquals(tournament['start_datetime'], self.START_DATETIME, 'Start datetime did not match')
