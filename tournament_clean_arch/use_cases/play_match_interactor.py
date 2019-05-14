class PlayMatchInteractor(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
        self.user_id = None
        self.round_number = None
        self.tournament_id = None

    def setup(self, user_id, round_number, tournament_id):
        self.user_id = user_id
        self.round_number = round_number
        self.tournament_id = tournament_id

    def execute(self):
        return
