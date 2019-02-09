class CreateTournamentInteractor(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
        self.no_of_rounds = 0
        self.start_datetime = ''

    def setup(self, no_of_rounds, start_datetime):
        self.no_of_rounds = no_of_rounds
        self.start_datetime = start_datetime

    def execute(self):
        tournament_id = self.storage.create_tournament(
            self.no_of_rounds,
            self.start_datetime
        )
        tournament_data = self.storage.get_tournament(
            tournament_id
        )
        return self.presenter.present_create_tournament(
            tournament_data
        )