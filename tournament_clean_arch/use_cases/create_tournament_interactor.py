class CreateTournamentInteractor(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
        self.no_of_rounds = None
        self.start_datetime = None

    def setup(self, no_of_rounds, start_datetime):
        self.no_of_rounds = no_of_rounds
        self.start_datetime = start_datetime

    @staticmethod
    def validate_no_of_rounds(no_of_rounds):
        if no_of_rounds < 3:
            from tournament_clean_arch.exceptions.custom_exceptions import \
                InvalidNumberOfRounds
            raise InvalidNumberOfRounds

    @staticmethod
    def validate_start_datetime(start_datetime):
        import datetime
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        if start_datetime < now:
            from tournament_clean_arch.exceptions.custom_exceptions import \
                InvalidStartDateTimeForTournament
            raise InvalidStartDateTimeForTournament

    def execute(self):
        self.validate_no_of_rounds(no_of_rounds=self.no_of_rounds)
        self.validate_start_datetime(start_datetime=self.start_datetime)

        tournament_id = self.storage.create_tournament(
            no_of_rounds=self.no_of_rounds,
            start_datetime=self.start_datetime,
        )
        tournament_details = self.storage.get_tournament(
            tournament_id=tournament_id)

        return self.presenter.present_create_tournament(
            tournament_details=tournament_details)
