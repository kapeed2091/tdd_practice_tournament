from freezegun import freeze_time
from display_reports.constants.general import TransactionStatus


@freeze_time('2019-03-10 12:00:00')
def test_create_payment_reports():
    import datetime
    payment_reports_data = [
        {
            "ref_no": "Ref1234",
            "amount": 100,
            "transaction_status": TransactionStatus.SUCCESS.value,
            "transaction_datetime": datetime.datetime.now(),
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
