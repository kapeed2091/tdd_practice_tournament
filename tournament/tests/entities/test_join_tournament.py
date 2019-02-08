from unittest import TestCase


class TestJoinTournament(TestCase):
    import datetime
    NO_OF_ROUNDS = 4
    START_DATETIME = datetime.datetime.now()
    USERNAME = 'deepak'

    def setUp(self):
        from tournament.entities import Tournament
        self.tournament_obj = Tournament(
            no_of_rounds=self.NO_OF_ROUNDS, start_datetime=self.START_DATETIME)

    def test_join_tournament(self):
        self.tournament_obj.join_tournament(username=self.USERNAME)
        self.assertIn(self.USERNAME, self.tournament_obj.usernames,
                      'User did not subscribe')
