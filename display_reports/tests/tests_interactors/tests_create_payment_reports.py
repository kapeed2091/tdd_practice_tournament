from freezegun import freeze_time
from mock import create_autospec
from display_reports.constants.general import TransactionStatus


@freeze_time('2019-03-10 12:00:00')
def test_create_payment_reports():
    import datetime
    from display_reports.interactors.payment_report_interactor import PaymentReportInteractor
    payment_report_utils = PaymentReportInteractor()
    payment_reports_data = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "transaction_status": TransactionStatus.SUCCESS.value,
            "transaction_datetime": datetime.datetime.now(),
            "franchise_id": 1
        }
    ]

    from display_reports.storage.storage import Storage
    storage_mock = create_autospec(Storage)

    payment_report_utils.create_payment_reports(
        payment_reports_data=payment_reports_data,
        storage=storage_mock
    )
    storage_mock.create_payment_reports.assert_called_once_with(payment_reports_data)
