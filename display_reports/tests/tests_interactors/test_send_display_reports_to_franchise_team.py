from mock import create_autospec


def test_send_display_reports_to_franchise_team():
    from datetime import datetime
    from display_reports.interactors.storage.storage import Storage
    from display_reports.interactors.display_report_interactor import DisplayReportInteractor

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=15).date()
    }
    franchise_ids = [1, 2, 3]

    storage_mock = create_autospec(Storage)
    display_report_interactor = DisplayReportInteractor(
        date_range=date_range, franchise_ids=franchise_ids,
        storage=storage_mock)
    display_report_interactor.send_display_reports_to_franchise_team()

    storage_mock.send_display_reports_to_franchise_team.assert_called_once_with(
        date_range=date_range, franchise_ids=franchise_ids
    )
