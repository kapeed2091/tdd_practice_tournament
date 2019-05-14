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
        matched_payment_reports = []
        for sale_report in sale_reports:
            display_report = None
            for payment_report in payment_reports:
                display_report = self._get_mapped_display_report(
                    sale_report=sale_report, payment_report=payment_report
                )
                if display_report:
                    display_reports.append(display_report)
                    matched_payment_reports.append(payment_report)
                    break
            if not display_report:
                display_report = self._get_extra_sale_display_report(sale_report)
                display_reports.append(display_report)
        un_matched_payment_reports = [payment_report for payment_report in payment_reports
                                      if payment_report not in matched_payment_reports]
        un_billed_display_reports = self._get_unbilled_display_reports(
            un_matched_payment_reports
        )
        display_reports += un_billed_display_reports
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

    @staticmethod
    def _get_extra_sale_display_report(sale_report):
        return {
            "sale_report_ref_no": sale_report['ref_no'],
            "payment_report_ref_no": None,
            "sale_report_amount": sale_report['amount'],
            "payment_report_amount": None,
            "status": DisplayReportStatus.EXTRA_SALE.value
        }

    @staticmethod
    def _get_unbilled_display_reports(payment_reports):
        return [
            {
                "sale_report_ref_no": None,
                "payment_report_ref_no": payment_report['ref_no'],
                "sale_report_amount": None,
                "payment_report_amount": payment_report['amount'],
                "status": DisplayReportStatus.UN_BILLED.value
            } for payment_report in payment_reports
        ]
