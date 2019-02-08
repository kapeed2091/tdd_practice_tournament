class Tournament(object):
    def __init__(self, no_of_rounds, start_datetime):
        self.no_of_rounds = no_of_rounds
        self.start_datetime = start_datetime
        self.player_usernames = []
        self.matches = []

    @staticmethod
    def create(no_of_rounds, start_datetime):
        return Tournament(no_of_rounds=no_of_rounds,
                          start_datetime=start_datetime)

    def join(self, username):
        self._validate_join(username=username)
        self._add_player(username)

    def create_matches_for_first_round(self):
        pass

    def _validate_join(self, username):
        if self._is_username_already_joined(username):
            from tournament.exceptions import JoinTournamentDuplicateUser
            raise JoinTournamentDuplicateUser(
                'User cannot join a tournament multiple times')

        if self._is_full():
            from tournament.exceptions import \
                JoinTournamentMaximumCountExceeded
            raise JoinTournamentMaximumCountExceeded('Tournament is full')

    def _is_username_already_joined(self, username):
        return username in self.player_usernames

    def _is_full(self):
        return len(self.player_usernames) == 2 ** self.no_of_rounds

    def _add_player(self, username):
        self.player_usernames.append(username)
