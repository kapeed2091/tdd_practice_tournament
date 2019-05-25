import abc


class Presenter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_display_reports(self, display_reports_data):
        pass
