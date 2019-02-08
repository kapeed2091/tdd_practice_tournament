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

    def test_join_tournament_for_duplicate_username(self):
        self.tournament_obj.usernames.append(self.USERNAME)
        from tournament.exceptions import JoinTournamentDuplicateUser
        with self.assertRaises(JoinTournamentDuplicateUser):
            self.tournament_obj.join_tournament(username=self.USERNAME)

    def test_join_tournament_to_check_maximum_count(self):
        subscribed_usernames = ['USERNAME_'+str(i+1) for i in range(
            0, 2**self.NO_OF_ROUNDS)]
        self.tournament_obj.usernames.extend(subscribed_usernames)
        from tournament.exceptions import JoinTournamentMaximumCountExceeded
        with self.assertRaises(JoinTournamentMaximumCountExceeded):
            self.tournament_obj.join_tournament(username=self.USERNAME)
