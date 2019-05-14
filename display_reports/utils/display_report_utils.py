from display_reports.constants.general import DisplayReportStatus


class DisplayReportUtils(object):

    def generate_display_reports(self, date_range, franchise_ids, storage):
        sale_reports = storage.get_sale_reports(date_range=date_range,
                                                franchise_ids=franchise_ids)
        payment_reports = storage.get_payment_reports(date_range=date_range,
                                                      franchise_ids=franchise_ids)

        display_reports = self._get_matched_display_reports(
            sale_reports=sale_reports, payment_reports=payment_reports)
        storage.create_display_reports(display_reports)

    @staticmethod
    def _get_matched_display_reports(sale_reports, payment_reports):
        display_reports = []
        for sale_report in sale_reports:
            sale_report_ref_no = sale_report['ref_no']
            sale_report_amount = sale_report['amount']

            for payment_report in payment_reports:
                if sale_report_ref_no == payment_report['ref_no'] and \
                        sale_report_amount == payment_report['amount']:
                    display_reports.append(
                        {
                            "ref_no": sale_report_ref_no,
                            "amount": sale_report_amount,
                            "status": DisplayReportStatus.MATCHED.value
                        }
                    )
                break
        return display_reports
