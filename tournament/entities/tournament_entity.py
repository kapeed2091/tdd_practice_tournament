class Tournament(object):
    def __init__(self, no_of_rounds, start_datetime):
        self.no_of_rounds = no_of_rounds
        self.start_datetime = start_datetime
        self.usernames = []

    @staticmethod
    def create_tournament(no_of_rounds, start_datetime):
        return Tournament(no_of_rounds=no_of_rounds,
                          start_datetime=start_datetime)

    def join_tournament(self, username):
        self._validate_join_tournament(username=username)
        self.usernames.append(username)

    def _validate_join_tournament(self, username):
        if self._is_username_already_joined(username):
            from tournament.exceptions import JoinTournamentDuplicateUser
            raise JoinTournamentDuplicateUser(
                'User cannot join a tournament multiple times')

        if self._is_tournament_full():
            from tournament.exceptions import \
                JoinTournamentMaximumCountExceeded
            raise JoinTournamentMaximumCountExceeded('Tournament is full')

    def _is_username_already_joined(self, username):
        return username in self.usernames

    def _is_tournament_full(self):
        return len(self.usernames) == 2**self.no_of_rounds
