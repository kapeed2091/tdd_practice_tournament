class CreateMatchesInTournamentInteractor(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def setup(self, tournament_id):
        pass

    def execute(self):
        self.storage.create_matches([])
        pass
