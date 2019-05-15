from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    # ---------MOCK IMPLEMENTATION---------
    try:
        from display_reports.views.upload_payment_reports.tests.test_case_01 \
            import TEST_CASE as test_case
    except ImportError:
        from display_reports.views.upload_payment_reports.tests.test_case_01 \
            import test_case

    from django_swagger_utils.drf_server.utils.server_gen.mock_response \
        import mock_response
    try:
        from display_reports.views.upload_payment_reports.request_response_mocks \
            import RESPONSE_200_JSON
    except ImportError:
        RESPONSE_200_JSON = ''
    response_tuple = mock_response(
        app_name="display_reports", test_case=test_case,
        operation_name="upload_payment_reports",
        kwargs=kwargs, default_response_body=RESPONSE_200_JSON)
    return response_tuple[1]


def get_display_reports_from_csv(file_path):
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
