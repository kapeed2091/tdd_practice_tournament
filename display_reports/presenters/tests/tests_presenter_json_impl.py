from display_reports.constants.general import DisplayReportStatus


def test_get_display_reports():
    display_reports_data = [
        {
            "sale_report_reference_no": "Ref1",
            "payment_report_reference_no": "Ref1",
            "sale_report_amount": 100,
            "payment_report_amount": 100,
            "status": DisplayReportStatus.MATCHED.value
        }
    ]

    presenter_json_impl = PresenterJsonImpl()
    display_reports_response = \
        presenter_json_impl.get_display_reports(display_reports_data)
    assert display_reports_response == display_reports_data
