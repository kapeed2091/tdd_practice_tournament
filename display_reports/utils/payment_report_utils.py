class PaymentReportUtils(object):

    @staticmethod
    def create_payment_reports(payment_reports_data, storage):
        storage.create_payment_reports(
            payment_reports_data=payment_reports_data
        )
