import abc


class Storage(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_payment_reports(self, payment_reports_data):
        pass

    @abc.abstractmethod
    def get_sale_reports(self, date_range, franchise_ids):
        pass

    @abc.abstractmethod
    def get_payment_reports(self, date_range, franchise_ids):
        pass

    @abc.abstractmethod
    def create_display_reports(self, display_reports):
        pass
