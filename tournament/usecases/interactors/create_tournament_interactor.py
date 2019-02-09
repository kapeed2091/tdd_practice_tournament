class CreateTournamentInteractor(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
        self.no_of_rounds = 0
        self.start_datetime = ''

    def setup(self, no_of_rounds, start_datetime):
        self.no_of_rounds = no_of_rounds
        self.start_datetime = start_datetime

    def _validate_no_of_rounds(self):
        if self.no_of_rounds < 3:
            raise Exception("No of rounds is less than 3")

    def _validate_start_datetime(self):
        import datetime
        if datetime.datetime.strptime(self.start_datetime, '%m/%d/%Y, %H:%M:%S') < datetime.datetime.now():
            raise Exception("Start datetime can not be less than current datetime")

    def execute(self):
        self._validate_no_of_rounds()
        self._validate_start_datetime()

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