import abc


class Storage(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_payment_reports(self, payment_reports_data):
        pass
