from display_reports.storage.storage import Storage


class StorageImplementation(Storage):

    def send_display_reports_to_franchise_team(self, display_reports_data):
        pass

    def get_display_reports(self, date_range, franchise_ids):
        pass

    def create_display_reports(self, display_reports):
        pass

    def get_payment_reports(self, date_range, franchise_ids):
        pass

    def get_sale_reports(self, date_range, franchise_ids):
        pass

    def create_payment_reports(self, payment_reports_data):
        pass