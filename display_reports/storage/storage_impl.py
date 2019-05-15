from display_reports.storage.storage import Storage


class StorageImplementation(Storage):

    def send_display_reports_to_franchise_team(self, display_reports_data):
        pass

    def get_display_reports(self, date_range, franchise_ids):
        pass

    def create_display_reports(self, display_reports):
        from display_reports.models import DisplayReport
        display_report_objects = [
            DisplayReport(
                sale_report_reference_no=display_report['sale_report_ref_no'],
                payment_report_reference_no=display_report['payment_report_ref_no'],
                sale_report_amount=display_report['sale_report_amount'],
                payment_report_amount=display_report['payment_report_amount'],
                franchise_id=display_report['franchise_id'],
                status=display_report['status']
            ) for display_report in display_reports
        ]
        DisplayReport.objects.bulk_create(display_report_objects)

    def get_payment_reports(self, date_range, franchise_ids):
        from display_reports.models import PaymentReport
        payment_reports = PaymentReport.objects.filter(
            transaction_datetime__date__lte=date_range['to_date'],
            transaction_datetime__date__gte=date_range['from_date'],
            franchise_id__in=franchise_ids
        )
        return [
            {
                "ref_no": payment_report.reference_no,
                "amount": payment_report.amount,
                "franchise_id": payment_report.franchise_id
            } for payment_report in payment_reports
        ]

    def get_sale_reports(self, date_range, franchise_ids):
        from display_reports.models import SaleReport
        sale_reports = SaleReport.objects.filter(
            transaction_datetime__date__lte=date_range['to_date'],
            transaction_datetime__date__gte=date_range['from_date'],
            franchise_id__in=franchise_ids
        )
        return [
            {
                "ref_no": sale_report.reference_no,
                "amount": sale_report.amount,
                "franchise_id": sale_report.franchise_id
            } for sale_report in sale_reports
        ]

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
