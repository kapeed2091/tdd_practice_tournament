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

    from display_reports.presenters.preseenter_csv_impl import PresenterCsvImpl
    presenter_csv_impl = PresenterCsvImpl()
    file_path = presenter_csv_impl.get_display_reports(display_reports_data)
    assert file_path is not None
