class Tournament(object):
    def __init__(self):
        self.no_of_rounds = None
        self.start_datetime = None

    @staticmethod
    def create_tournament(no_of_rounds, start_datetime):
        return Tournament()
