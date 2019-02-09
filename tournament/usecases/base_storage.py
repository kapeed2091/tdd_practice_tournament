import abc


class BaseStorage(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def create_tournament(self, no_of_rounds, start_datetime):
        pass

    @abc.abstractmethod
    def get_tournament(self, tournament_id):
        pass

    @abc.abstractmethod
    def create_matches(self, matches):
        pass
