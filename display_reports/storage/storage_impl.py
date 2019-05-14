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
        from display_reports.models import PaymentReport
        payment_report_objects = [
            PaymentReport(
                reference_no=payment_report_data['ref_no'],
                amount=payment_report_data['amount'],
                transaction_status=payment_report_data['transaction_status'],
                transaction_datetime=payment_report_data['transaction_datetime'],
                franchise_id=payment_report_data['franchise_id']
            ) for payment_report_data in payment_reports_data
        ]

        PaymentReport.objects.bulk_create(payment_report_objects)
