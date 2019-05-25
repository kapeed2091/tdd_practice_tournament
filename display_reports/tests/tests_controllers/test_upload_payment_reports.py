from django.conf import settings
import os

def test_convert_payment_report_csv_file():
    from datetime import datetime
    from display_reports.views.upload_payment_reports.api_wrapper import get_payment_reports_from_csv

    file_path = os.path.join(settings.BASE_DIR, "display_reports", "tests", "tests_controllers", "test_files", "payment_report_test_file.csv")

    display_reports = get_payment_reports_from_csv(file_path)

    display_reports_expected = [
        {
            "ref_no": "Ref123",
            "amount": 100,
            "transaction_status": "SUCCESS",
            "transaction_datetime": datetime(year=2018, month=03, day=10, hour=9),
            "franchise_id": 1
        },
        {
            "ref_no": "Ref234",
            "amount": 150,
            "transaction_status": "SUCCESS",
            "transaction_datetime": datetime(year=2018, month=03, day=12, hour=8),
            "franchise_id": 2
        }
    ]
    assert display_reports == display_reports_expected
