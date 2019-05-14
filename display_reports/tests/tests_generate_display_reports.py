from mock import create_autospec


def test_generate_display_reports_with_status_matched():
    from datetime import datetime
    from display_reports.storage.storage import Storage
    from display_reports.utils.display_report_utils import DisplayReportUtils

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    display_report_utils = DisplayReportUtils()
    storage_mock = create_autospec(Storage)
    display_report_utils.generate_display_reports(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock
    )

    storage_mock.generate_display_reports.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
