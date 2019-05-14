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
        user_tournament_id = self.storage.create_user_tournament(
            user_id=self.user_id,
            tournament_id=self.tournament_id
        )

        presenter_details = self.presenter.present_create_user_tournament(
            user_tournament_id=user_tournament_id
        )
        return presenter_details
