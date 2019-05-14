from freezegun import freeze_time
import mock


@freeze_time('2019-03-10 12:00:00')
def test_create_payment_reports():
    import datetime
    payment_report_utils = PaymentReportUtils()
    payment_reports_data = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "transaction_status": TransactionStatus.SUCCESS.value,
            "transaction_datetime": datetime.datetime.now()
        }
    ]

    with mock.patch.object(Storage, 'create_payment_reports', return_value=None) as storage_mock:
        storage = Storage()
        payment_report_utils.create_payment_reports(
            payment_reports_data=payment_reports_data,
            storage=storage
        )
        storage_mock.assert_called_once_with(payment_reports_data)
