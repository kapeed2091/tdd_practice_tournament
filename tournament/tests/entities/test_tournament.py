from unittest import TestCase


class TestTournament(TestCase):
    import datetime
    NO_OF_ROUNDS = 4
    START_DATETIME = datetime.datetime.now()

    def test_create_tournament(self):
        from tournament.entities import Tournament
        tournament_obj = Tournament.create_tournament(
            no_of_rounds=self.NO_OF_ROUNDS, start_datetime=self.START_DATETIME)

        self.assertEquals(tournament_obj.no_of_rounds, self.NO_OF_ROUNDS,
                          'Number of rounds did not match')
        self.assertEquals(tournament_obj.start_datetime, self.START_DATETIME,
                          'Start Datetime did not match')
