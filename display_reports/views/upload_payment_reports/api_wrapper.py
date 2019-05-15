from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from display_reports.interactors.payment_report_interactor import PaymentReportInteractor
    from display_reports.storage.storage_impl import StorageImplementation

    request_data = kwargs['request_data']
    file_path = request_data['file_path']
    payment_reports = get_payment_reports_from_csv(file_path)
    payment_report_interactor = PaymentReportInteractor()
    storage = StorageImplementation()

    payment_report_interactor.create_payment_reports(
        payment_reports_data=payment_reports, storage=storage)
    return


def get_payment_reports_from_csv(file_path):
    import csv
    from datetime import datetime
    from display_reports.constants.general import PAYMENT_REPORT_TRANSACTION_DATETIME_FORMAT

    datetime_fields = ['transaction_datetime']
    integer_fields = ['franchise_id']
    float_fields = ['amount']
    csv_reader = csv.DictReader(open(file_path))
    display_reports = []
    for row in csv_reader:
        for datetime_field in datetime_fields:
            datetime_str = row[datetime_field]
            row[datetime_field] = datetime.strptime(
                datetime_str, PAYMENT_REPORT_TRANSACTION_DATETIME_FORMAT)

        for integer_field in integer_fields:
            row[integer_field] = int(row[integer_field])

        for float_field in float_fields:
            row[float_field] = float(row[float_field])
        display_reports.append(row)
    return display_reports
