from freezegun import freeze_time
from mock import Mock
from display_reports.constants.general import TransactionStatus


@freeze_time('2019-03-10 12:00:00')
def test_create_payment_reports():
    import datetime
    from display_reports.utils.payment_report_utils import PaymentReportUtils
    payment_report_utils = PaymentReportUtils()
    payment_reports_data = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "transaction_status": TransactionStatus.SUCCESS.value,
            "transaction_datetime": datetime.datetime.now()
        }
    ]

    from display_reports.storage.storage import Storage
    storage_mock = Mock({"create_payment_reports": None}, Storage, spec_set=True)

    payment_report_utils.create_payment_reports(
        payment_reports_data=payment_reports_data,
        storage=storage_mock
    )
    storage_mock.assert_called_once_with(payment_reports_data)
