from display_reports.constants.general import DisplayReportStatus


class DisplayReportUtils(object):

    def generate_display_reports(self, date_range, franchise_ids, storage):
        sale_reports = storage.get_sale_reports(date_range=date_range,
                                                franchise_ids=franchise_ids)
        payment_reports = storage.get_payment_reports(date_range=date_range,
                                                      franchise_ids=franchise_ids)

        display_reports = self._get_display_reports(
            sale_reports=sale_reports, payment_reports=payment_reports)
        storage.create_display_reports(display_reports)

    def _get_display_reports(self, sale_reports, payment_reports):
        display_reports = []
        for sale_report in sale_reports:
            for payment_report in payment_reports:
                display_report = self._get_mapped_display_report(
                    sale_report=sale_report, payment_report=payment_report
                )
                if display_report:
                    display_reports.append(display_report)

        return display_reports

    @staticmethod
    def _get_mapped_display_report(sale_report, payment_report):
        sale_report_ref_no = sale_report['ref_no']
        sale_report_amount = sale_report['amount']
        status = None
        display_report = None
        if sale_report_ref_no == payment_report['ref_no']:
            status = DisplayReportStatus.MATCHED.value \
                if sale_report_amount == payment_report['amount'] else \
                DisplayReportStatus.AMOUNT_MISMATCH.value
        elif sale_report_amount == payment_report['amount']:
            status = DisplayReportStatus.REF_NO_MISMATCH.value

        if status:
            display_report = {
                "sale_report_ref_no": sale_report_ref_no,
                "payment_report_ref_no": payment_report['ref_no'],
                "sale_report_amount": sale_report_amount,
                "payment_report_amount": payment_report['amount'],
                "status": status
            }
        return display_report
