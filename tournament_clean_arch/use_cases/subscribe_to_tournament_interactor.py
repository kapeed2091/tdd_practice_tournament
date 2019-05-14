class SubscribeToTournamentInteractor(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
        self.user_id = None
        self.tournament_id = None

    def setup(self, user_id, tournament_id):
        self.user_id = user_id
        self.tournament_id = tournament_id

    def validate_tournament_has_started(self, tournament_id):
        tournament_details = self.storage.get_tournament(
            tournament_id=tournament_id
        )
        start_datetime = tournament_details["start_datetime"]

        import datetime
        now = datetime.datetime.now()

        if start_datetime < now:
            from tournament_clean_arch.exceptions.custom_exceptions import \
                TournamentHasStarted
            raise TournamentHasStarted

    def execute(self):
        self.validate_tournament_has_started(
            tournament_id=self.tournament_id
        )
        subscribe_id = self.storage.subscribe_to_tournament(
            user_id=self.user_id,
            tournament_id=self.tournament_id
        )

        presenter_details = self.presenter.present_subscribe_to_tournament(
            subscribe_id=subscribe_id
        )
        return presenter_details
