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
        match_id = self.storage.get_unassigned_match_for_round(
            round_number=self.round_number,
            tournament_id=self.tournament_id
        )

        user_match_id = self.storage.assign_match_to_user(
            match_id=match_id, user_id=self.user_id
        )

        presenter_details = self.presenter.present_play_match(
            user_match_id=user_match_id
        )
        return presenter_details
