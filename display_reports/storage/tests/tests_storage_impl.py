import pytest
import pytz
from freezegun import freeze_time
from display_reports.constants.general import TransactionStatus, DisplayReportStatus


@freeze_time('2019-03-10 12:00:00')
@pytest.mark.django_db
def test_create_payment_reports():
    from display_reports.storage.storage_impl import StorageImplementation
    from display_reports.models import PaymentReport
    import datetime
    payment_reports_data = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "transaction_status": TransactionStatus.SUCCESS.value,
            "transaction_datetime": pytz.utc.localize(datetime.datetime.now()),
            "franchise_id": 1
        }
    ]

    storage_impl = StorageImplementation()
    storage_impl.create_payment_reports(payment_reports_data)
    payment_reports = PaymentReport.objects.all()
    assert len(payment_reports) == 1
    payment_reports_data_created = [
        {
            "ref_no": payment_report.reference_no,
            "amount": payment_report.amount,
            "transaction_status": payment_report.transaction_status,
            "transaction_datetime": payment_report.transaction_datetime,
            "franchise_id": payment_report.franchise_id
        } for payment_report in payment_reports
    ]
    assert payment_reports_data == payment_reports_data_created


@pytest.mark.django_db
def test_get_payment_reports():
    from datetime import datetime
    from display_reports.models import PaymentReport
    payment_report_objects = [
        PaymentReport(
            reference_no="Ref1",
            amount=100,
            transaction_status=TransactionStatus.SUCCESS.value,
            transaction_datetime=datetime(year=2019, month=03, day=10, hour=12),
            franchise_id=1
        ),
        PaymentReport(
            reference_no="Ref2",
            amount=100,
            transaction_status=TransactionStatus.SUCCESS.value,
            transaction_datetime=datetime(year=2019, month=03, day=10, hour=12),
            franchise_id=2
        ),
        PaymentReport(
            reference_no="Ref3",
            amount=100,
            transaction_status=TransactionStatus.SUCCESS.value,
            transaction_datetime=datetime(year=2019, month=03, day=10, hour=12),
            franchise_id=3
        ),
        PaymentReport(
            reference_no="Ref4",
            amount=100,
            transaction_status=TransactionStatus.SUCCESS.value,
            transaction_datetime=datetime(year=2019, month=03, day=15, hour=12),
            franchise_id=1
        )
    ]
    PaymentReport.objects.bulk_create(payment_report_objects)

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=14).date()
    }
    franchise_ids = [1, 2]

    from display_reports.storage.storage_impl import StorageImplementation
    storage_impl = StorageImplementation()
    payment_reports = storage_impl.get_payment_reports(
        date_range=date_range, franchise_ids=franchise_ids)
    payment_report_expected = [
        {
            "ref_no": "Ref1",
            "amount": 100
        },
        {
            "ref_no": "Ref2",
            "amount": 100
        }
    ]
    assert payment_report_expected == payment_reports


@pytest.mark.django_db
def test_create_display_reports():
    from display_reports.models import DisplayReport
    from display_reports.storage.storage_impl import StorageImplementation
    display_reports_data = [
        {
            "sale_report_ref_no": "Ref1234",
            "payment_report_ref_no": "Ref1234",
            "sale_report_amount": 100,
            "payment_report_amount": 100,
            "status": DisplayReportStatus.MATCHED.value
        }
    ]

    storage_impl = StorageImplementation()
    storage_impl.create_display_reports(display_reports_data)
    display_reports = DisplayReport.objects.all()
    assert len(display_reports) == 1
    display_reports_data_created = [
        {
            "sale_report_ref_no": display_report.sale_report_reference_no,
            "payment_report_ref_no": display_report.payment_report_reference_no,
            "sale_report_amount": display_report.sale_report_amount,
            "payment_report_amount": display_report.payment_report_amount,
            "status": display_report.status
        } for display_report in display_reports
    ]
    assert display_reports_data == display_reports_data_created
