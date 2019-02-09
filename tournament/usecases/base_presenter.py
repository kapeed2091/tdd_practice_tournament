import abc


class BasePresenter(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def present_create_tournament(self, output_data):
        pass
