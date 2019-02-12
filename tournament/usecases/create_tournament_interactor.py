class CreateTournamentInteractor(object):
    def __init__(self, storage=None, presenter=None):
        self.storage=storage
        self.presenter=presenter

    def setup(self, no_of_rounds, start_datetime):
        self.no_of_rounds = no_of_rounds
        self.start_datetime = start_datetime

    def execute(self):
        #processLogic
        tournament_id = self.storage.create_tournament(
            no_of_rounds=self.no_of_rounds, start_datetime=self.start_datetime)
        tournament_data = self.storage.get_tournament(tournament_id)
        #prepareData
        return self.presenter.present_create_tournament(tournament_data,
                                                        tournament_id)
