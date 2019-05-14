from mock import create_autospec

from display_reports.constants.general import DisplayReportStatus


def test_get_display_reports_for_selected_date_range_and_franchises():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    display_reports_data = [
        {
            "sale_report_ref_no": "Ref123",
            "payment_report_ref_no": "Ref123",
            "sale_report_amount": 100,
            "payment_report_amount": 100,
            "status": DisplayReportStatus.MATCHED.value
        },
        {
            "sale_report_ref_no": "Ref123",
            "payment_report_ref_no": "Ref123",
            "sale_report_amount": 100,
            "payment_report_amount": 150,
            "status": DisplayReportStatus.AMOUNT_MISMATCH.value
        }
    ]
    storage_mock.get_display_reports.return_value = display_reports_data

    from display_reports.presenters.presenter import Presenter
    presenter_mock = create_autospec(Presenter)
    presenter_mock.get_display_reports.return_value = None

    display_report_utils = DisplayReportUtils(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )
    display_report_utils.get_display_reports(presenter=presenter_mock)
    storage_mock.get_display_reports.assert_called_once_with(date_range=date_range,
                                                             franchise_ids=franchise_ids)

    presenter_mock.get_display_reports.assert_called_once_with(display_reports_data)