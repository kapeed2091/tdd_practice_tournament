import abc


class AbstractStorage(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_tournament(self, no_of_rounds, start_datetime):
        pass

