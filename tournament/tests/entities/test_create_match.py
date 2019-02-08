from unittest import TestCase


class TestCreateMatch(TestCase):
    import datetime
    NO_OF_ROUNDS = 4
    START_DATETIME = datetime.datetime.now()
    PLAYER_USERNAMES = ['USERNAME_'+str(i+1) for i in range(0, 2**NO_OF_ROUNDS)]

    def setUp(self):
        from tournament.entities import Tournament
        self.tournament_obj = Tournament(no_of_rounds=self.NO_OF_ROUNDS, start_datetime=self.START_DATETIME)
        self.tournament_obj.player_usernames = self.PLAYER_USERNAMES

    def test_create_matches_for_first_round(self):
        self.tournament_obj.create_matches_for_first_round()
        self.assertEquals(len(self.tournament_obj.matches), 2**(self.NO_OF_ROUNDS-1), 'First round matches count did not match')
