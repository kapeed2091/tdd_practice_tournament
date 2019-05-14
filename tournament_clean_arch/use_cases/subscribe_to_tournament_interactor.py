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

    def validate_if_tournament_is_full(self, tournament_id):
        tournament_details = self.storage.get_tournament(
            tournament_id=tournament_id
        )
        players_count = self.storage.get_total_subscribers_for_tournament(
            tournament_id=tournament_id
        )

        no_of_rounds = tournament_details["no_of_rounds"]

        from tournament_clean_arch.utils. \
            get_max_allowed_players_for_tournament import \
            get_max_allowed_players_for_tournament
        max_allowed_players_for_tournament = \
            get_max_allowed_players_for_tournament(no_of_rounds=no_of_rounds)

        if players_count >= max_allowed_players_for_tournament:
            from tournament_clean_arch.exceptions.custom_exceptions import \
                TournamentIsFull
            raise TournamentIsFull

    def validate_if_user_already_in_tournament(self, tournament_id, user_id):
        user_in_tournament = self.storage.is_user_in_tournament(
            tournament_id=tournament_id,
            user_id=user_id
        )
        if user_in_tournament:
            from tournament_clean_arch.exceptions.custom_exceptions import \
                UserAlreadySubscribed
            raise UserAlreadySubscribed

    def execute(self):
        self.validate_tournament_has_started(
            tournament_id=self.tournament_id
        )
        self.validate_if_tournament_is_full(tournament_id=self.tournament_id)
        self.validate_if_user_already_in_tournament(
            tournament_id=self.tournament_id,
            user_id=self.user_id
        )

        subscribe_id = self.storage.subscribe_to_tournament(
            user_id=self.user_id,
            tournament_id=self.tournament_id
        )

        presenter_details = self.presenter.present_subscribe_to_tournament(
            subscribe_id=subscribe_id
        )
        return presenter_details
