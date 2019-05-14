class SubscribeToTournamentInteractor(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
        self.user_id = None
        self.tournament_id = None

    def setup(self, user_id, tournament_id):
        self.user_id = user_id
        self.tournament_id = tournament_id

    def execute(self):
        subscribe_id = self.storage.subscribe_to_tournament(
            user_id=self.user_id,
            tournament_id=self.tournament_id
        )

        presenter_details = self.presenter.present_subscribe_to_tournament(
            subscribe_id=subscribe_id
        )
        return presenter_details
