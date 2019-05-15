"""
# Positive Test Case
"""

from django_swagger_utils.utils.test import CustomAPITestCase

from display_reports.constants.general import DisplayReportStatus
from display_reports.utils.convert_unicode_strings import convert_unicode_strings
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
{
    "date_range": {
        "from_date": "2019-03-10", 
        "to_date": "2019-03-15"
    }, 
    "franchise_ids": [
        1
    ]
}
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read", "write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
}


class TestCase01GetDisplayReportsAPITestCase(CustomAPITestCase):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def setUp(self):
        from datetime import datetime
        from display_reports.models import DisplayReport
        display_report_objects = [
            DisplayReport(
                sale_report_reference_no="Ref11",
                payment_report_reference_no="Ref11",
                sale_report_amount=100,
                payment_report_amount=100,
                status=DisplayReportStatus.MATCHED.value,
                transaction_datetime=datetime(year=2019, month=03, day=12, hour=12),
                franchise_id=1
            ),
            DisplayReport(
                sale_report_reference_no="Ref12",
                payment_report_reference_no="Ref12",
                sale_report_amount=100,
                payment_report_amount=100,
                status=DisplayReportStatus.MATCHED.value,
                transaction_datetime=datetime(year=2019, month=03, day=9, hour=12),
                franchise_id=1
            ),
            DisplayReport(
                sale_report_reference_no="Ref13",
                payment_report_reference_no="Ref13",
                sale_report_amount=100,
                payment_report_amount=100,
                status=DisplayReportStatus.MATCHED.value,
                transaction_datetime=datetime(year=2019, month=03, day=10, hour=12),
                franchise_id=1
            ),
            DisplayReport(
                sale_report_reference_no="Ref21",
                payment_report_reference_no="Ref21",
                sale_report_amount=100,
                payment_report_amount=100,
                status=DisplayReportStatus.MATCHED.value,
                transaction_datetime=datetime(year=2019, month=03, day=12, hour=12),
                franchise_id=2
            )
        ]
        DisplayReport.objects.bulk_create(display_report_objects)

    def test_case(self):
        response = self.default_test_case()
        response = convert_unicode_strings(response.json())

        display_reports_expected = [
            {
                "sale_report_reference_no": "Ref11",
                "payment_report_reference_no": "Ref11",
                "sale_report_amount": 100,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.MATCHED.value
            },
            {
                "sale_report_reference_no": "Ref13",
                "payment_report_reference_no": "Ref13",
                "sale_report_amount": 100,
                "payment_report_amount": 100,
                "status": DisplayReportStatus.MATCHED.value
            }
        ]
        response_expected = {
            "display_reports": display_reports_expected
        }

        self.assertEqual(response, response_expected)
