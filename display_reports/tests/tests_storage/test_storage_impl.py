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
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=1
        ),
        PaymentReport(
            reference_no="Ref2",
            amount=100,
            transaction_status=TransactionStatus.SUCCESS.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=2
        ),
        PaymentReport(
            reference_no="Ref3",
            amount=100,
            transaction_status=TransactionStatus.SUCCESS.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=3
        ),
        PaymentReport(
            reference_no="Ref4",
            amount=100,
            transaction_status=TransactionStatus.SUCCESS.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=15, hour=12)),
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
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12))
        },
        {
            "ref_no": "Ref2",
            "amount": 100,
            "franchise_id": 2,
            "transaction_datetime": pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12))
        }
    ]
    assert payment_report_expected == payment_reports


@pytest.mark.django_db
def test_create_display_reports():
    from datetime import datetime
    from display_reports.models import DisplayReport
    from display_reports.storage.storage_impl import StorageImplementation
    display_reports_data = [
        {
            "sale_report_ref_no": "Ref1234",
            "payment_report_ref_no": "Ref1234",
            "sale_report_amount": 100,
            "payment_report_amount": 100,
            "franchise_id": 1,
            "transaction_datetime": pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
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
            "franchise_id": display_report.franchise_id,
            "transaction_datetime": display_report.transaction_datetime,
            "status": display_report.status
        } for display_report in display_reports
    ]
    assert display_reports_data == display_reports_data_created


@pytest.mark.django_db
def test_get_sale_reports():
    from datetime import datetime
    from display_reports.models import SaleReport
    payment_report_objects = [
        SaleReport(
            reference_no="Ref1",
            amount=100,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=1
        ),
        SaleReport(
            reference_no="Ref2",
            amount=100,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=2
        ),
        SaleReport(
            reference_no="Ref3",
            amount=100,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=3
        ),
        SaleReport(
            reference_no="Ref4",
            amount=100,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=15, hour=12)),
            franchise_id=1
        )
    ]
    SaleReport.objects.bulk_create(payment_report_objects)

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=14).date()
    }
    franchise_ids = [1, 2]

    from display_reports.storage.storage_impl import StorageImplementation
    storage_impl = StorageImplementation()
    sale_reports = storage_impl.get_sale_reports(
        date_range=date_range, franchise_ids=franchise_ids)
    sale_report_expected = [
        {
            "ref_no": "Ref1",
            "amount": 100,
            "franchise_id": 1,
            "transaction_datetime": pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12))
        },
        {
            "ref_no": "Ref2",
            "amount": 100,
            "franchise_id": 2,
            "transaction_datetime": pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12))
        }
    ]
    assert sale_report_expected == sale_reports


@pytest.mark.django_db
def test_get_display_reports():
    from datetime import datetime
    from display_reports.models import DisplayReport
    payment_report_objects = [
        DisplayReport(
            sale_report_reference_no="Ref1",
            payment_report_reference_no="Ref1",
            sale_report_amount=100,
            payment_report_amount=100,
            status=DisplayReportStatus.MATCHED.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=1
        ),
        DisplayReport(
            sale_report_reference_no="Ref2",
            payment_report_reference_no="Ref2",
            sale_report_amount=100,
            payment_report_amount=100,
            status=DisplayReportStatus.MATCHED.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=2
        ),
        DisplayReport(
            sale_report_reference_no="Ref3",
            payment_report_reference_no="Ref3",
            sale_report_amount=100,
            payment_report_amount=100,
            status=DisplayReportStatus.MATCHED.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=3
        ),
        DisplayReport(
            sale_report_reference_no="Ref4",
            payment_report_reference_no="Ref4",
            sale_report_amount=100,
            payment_report_amount=100,
            status=DisplayReportStatus.MATCHED.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=15, hour=12)),
            franchise_id=1
        )
    ]
    DisplayReport.objects.bulk_create(payment_report_objects)

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=14).date()
    }
    franchise_ids = [1, 2]

    from display_reports.storage.storage_impl import StorageImplementation
    storage_impl = StorageImplementation()
    display_reports = storage_impl.get_display_reports(
        date_range=date_range, franchise_ids=franchise_ids)
    display_reports_expected = [
        {
            "sale_report_reference_no": "Ref1",
            "payment_report_reference_no": "Ref1",
            "sale_report_amount": 100,
            "payment_report_amount": 100,
            "status": DisplayReportStatus.MATCHED.value,
        },
        {
            "sale_report_reference_no": "Ref2",
            "payment_report_reference_no": "Ref2",
            "sale_report_amount": 100,
            "payment_report_amount": 100,
            "status": DisplayReportStatus.MATCHED.value,
        }
    ]
    assert display_reports_expected == display_reports


@pytest.mark.django_db
def test_send_display_reports_to_franchise_team():
    from datetime import datetime
    from display_reports.models import DisplayReport
    payment_report_objects = [
        DisplayReport(
            sale_report_reference_no="Ref1",
            payment_report_reference_no="Ref1",
            sale_report_amount=100,
            payment_report_amount=100,
            status=DisplayReportStatus.MATCHED.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=1
        ),
        DisplayReport(
            sale_report_reference_no="Ref2",
            payment_report_reference_no="Ref2",
            sale_report_amount=100,
            payment_report_amount=100,
            status=DisplayReportStatus.MATCHED.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=2
        ),
        DisplayReport(
            sale_report_reference_no="Ref3",
            payment_report_reference_no="Ref3",
            sale_report_amount=100,
            payment_report_amount=100,
            status=DisplayReportStatus.MATCHED.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=10, hour=12)),
            franchise_id=3
        ),
        DisplayReport(
            sale_report_reference_no="Ref4",
            payment_report_reference_no="Ref4",
            sale_report_amount=100,
            payment_report_amount=100,
            status=DisplayReportStatus.MATCHED.value,
            transaction_datetime=pytz.utc.localize(datetime(year=2019, month=03, day=15, hour=12)),
            franchise_id=1
        )
    ]
    DisplayReport.objects.bulk_create(payment_report_objects)

    date_range = {
        "from_date": datetime(year=2019, month=03, day=10).date(),
        "to_date": datetime(year=2019, month=03, day=14).date()
    }
    franchise_ids = [1, 2]

    from display_reports.storage.storage_impl import StorageImplementation
    storage_impl = StorageImplementation()
    storage_impl.send_display_reports_to_franchise_team(
        date_range=date_range, franchise_ids=franchise_ids)

    display_reports = DisplayReport.objects.filter(
        transaction_datetime__date__lte=date_range['to_date'],
        transaction_datetime__date__gte=date_range['from_date'],
        franchise_id__in=franchise_ids
    )

    for display_report in display_reports:
        assert display_report.sent_to_franchise_team is True
