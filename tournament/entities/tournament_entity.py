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
        if username in self.usernames:
            from tournament.exceptions import JoinTournamentDuplicateUser
            raise JoinTournamentDuplicateUser(
                'User cannot join a tournament multiple times')
        self.usernames.append(username)
