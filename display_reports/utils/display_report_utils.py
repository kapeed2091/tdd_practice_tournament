from display_reports.constants.general import DisplayReportStatus


class DisplayReportUtils(object):

    def send_display_reports_to_franchise_team(self, date_range, franchise_ids, storage):
        display_reports = storage.get_display_reports(date_range=date_range,
                                                      franchise_ids=franchise_ids)
        storage.send_display_reports_to_franchise_team(display_reports)

    def get_display_reports(self, date_range, franchise_ids, storage, presenter):
        display_reports = storage.get_display_reports(date_range=date_range,
                                                      franchise_ids=franchise_ids)
        return presenter.get_display_reports(display_reports)

    def generate_display_reports(self, date_range, franchise_ids, storage):
        sale_reports = storage.get_sale_reports(date_range=date_range,
                                                franchise_ids=franchise_ids)
        payment_reports = storage.get_payment_reports(date_range=date_range,
                                                      franchise_ids=franchise_ids)

        display_reports = self._get_display_reports(
            sale_reports=sale_reports, payment_reports=payment_reports)
        storage.create_display_reports(display_reports)

    def _get_display_reports(self, sale_reports, payment_reports):
        un_matched_sale_reports, un_matched_payment_reports, matched_display_reports = \
            self._get_matched_display_reports(sale_reports=sale_reports,
                                              payment_reports=payment_reports)
        un_matched_sale_reports, un_matched_payment_reports, amount_mismatch_display_reports = \
            self._get_amount_mismatch_display_reports(
                sale_reports=un_matched_sale_reports,
                payment_reports=un_matched_payment_reports)
        un_matched_sale_reports, un_matched_payment_reports, ref_no_mismatch_display_reports = \
            self._get_ref_no_mismatch_display_reports(
                sale_reports=un_matched_sale_reports,
                payment_reports=un_matched_payment_reports)
        extra_sale_display_reports = self._get_extra_sale_display_reports(un_matched_sale_reports)
        unbilled_display_reports = self._get_unbilled_display_reports(un_matched_payment_reports)

        return matched_display_reports + amount_mismatch_display_reports + \
               ref_no_mismatch_display_reports + extra_sale_display_reports + \
               unbilled_display_reports


    def _get_matched_display_reports(self, sale_reports, payment_reports):
        matched_payment_reports = []
        matched_sale_reports = []
        display_reports = []
        for sale_report in sale_reports:
            sale_report_ref_no = sale_report['ref_no']
            sale_report_amount = sale_report['amount']
            matched_payment_report = None
            for payment_report in payment_reports:
                if sale_report_ref_no == payment_report['ref_no'] and \
                        sale_report_amount == payment_report['amount']:
                    matched_payment_report = payment_report
                    break
            if matched_payment_report:
                matched_payment_reports.append(matched_payment_report)
                matched_sale_reports.append(sale_report)
                display_report = self._get_display_report(
                    status=DisplayReportStatus.MATCHED.value,
                    sale_report=sale_report, payment_report=matched_payment_report
                )
                display_reports.append(display_report)
        un_matched_sale_reports = [sale_report for sale_report in sale_reports
                                   if sale_report not in matched_sale_reports]
        un_matched_payment_reports = [payment_report for payment_report in payment_reports
                                      if payment_report not in matched_payment_reports]
        return un_matched_sale_reports, un_matched_payment_reports, display_reports

    def _get_amount_mismatch_display_reports(self, sale_reports, payment_reports):
        matched_payment_reports = []
        matched_sale_reports = []
        display_reports = []
        for sale_report in sale_reports:
            sale_report_ref_no = sale_report['ref_no']
            sale_report_amount = sale_report['amount']
            matched_payment_report = None
            for payment_report in payment_reports:
                if sale_report_ref_no == payment_report['ref_no'] and \
                        sale_report_amount != payment_report['amount']:
                    matched_payment_report = payment_report
                    break
            if matched_payment_report:
                matched_payment_reports.append(matched_payment_report)
                matched_sale_reports.append(sale_report)
                display_report = self._get_display_report(
                    status=DisplayReportStatus.AMOUNT_MISMATCH.value,
                    sale_report=sale_report, payment_report=matched_payment_report
                )
                display_reports.append(display_report)
        un_matched_sale_reports = [sale_report for sale_report in sale_reports
                                   if sale_report not in matched_sale_reports]
        un_matched_payment_reports = [payment_report for payment_report in payment_reports
                                      if payment_report not in matched_payment_reports]
        return un_matched_sale_reports, un_matched_payment_reports, display_reports

    def _get_ref_no_mismatch_display_reports(self, sale_reports, payment_reports):
        matched_payment_reports = []
        matched_sale_reports = []
        display_reports = []
        for sale_report in sale_reports:
            sale_report_ref_no = sale_report['ref_no']
            sale_report_amount = sale_report['amount']
            matched_payment_report = None
            for payment_report in payment_reports:
                if sale_report_ref_no != payment_report['ref_no'] and \
                        sale_report_amount == payment_report['amount']:
                    matched_payment_report = payment_report
                    break
            if matched_payment_report:
                matched_payment_reports.append(matched_payment_report)
                matched_sale_reports.append(sale_report)
                display_report = self._get_display_report(
                    status=DisplayReportStatus.REF_NO_MISMATCH.value,
                    sale_report=sale_report, payment_report=matched_payment_report
                )
                display_reports.append(display_report)
        un_matched_sale_reports = [sale_report for sale_report in sale_reports
                                   if sale_report not in matched_sale_reports]
        un_matched_payment_reports = [payment_report for payment_report in payment_reports
                                      if payment_report not in matched_payment_reports]
        return un_matched_sale_reports, un_matched_payment_reports, display_reports

    def _get_extra_sale_display_reports(self, sale_reports):
        return [
            self._get_display_report(status=DisplayReportStatus.EXTRA_SALE.value,
                                     sale_report=sale_report)
            for sale_report in sale_reports
        ]

    def _get_unbilled_display_reports(self, payment_reports):
        return [
            self._get_display_report(status=DisplayReportStatus.UN_BILLED.value,
                                     payment_report=payment_report)
            for payment_report in payment_reports
        ]

    @staticmethod
    def _get_display_report(status, sale_report=None, payment_report=None):
        if sale_report or payment_report:
            display_report = {
                "sale_report_ref_no": sale_report['ref_no'] if sale_report else None,
                "sale_report_amount": sale_report['amount'] if sale_report else None,
                "payment_report_ref_no": payment_report['ref_no'] if payment_report else None,
                "payment_report_amount": payment_report['amount'] if payment_report else None,
                "status": status
            }
        else:
            display_report = None
        return display_report
