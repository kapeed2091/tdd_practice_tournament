class CreateTournamentUsecase(object):
    def __init__(self):
        self.no_of_rounds = 0
        self.start_datetime = ''

    def setup(self, no_of_rounds, start_datetime):
        self.no_of_rounds = no_of_rounds
        self.start_datetime = start_datetime
        pass

    def execute(self):
        return {'no_of_rounds': self.no_of_rounds,
                'start_datetime': self.start_datetime}
