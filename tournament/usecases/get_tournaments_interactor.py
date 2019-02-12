class GetTournamentsInteractor(object):
    def __init__(self, storage=None, presenter=None):
        self.storage = storage
        self.presenter = presenter

    def execute(self):
        #processLogic
        tournaments = self.storage.get_tournaments()
        #prepareData
        return self.presenter.present_get_tournaments(tournaments)
