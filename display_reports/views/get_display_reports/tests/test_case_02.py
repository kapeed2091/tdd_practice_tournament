"""
# Negative Test Case: Invalid Date Range
"""
from django_swagger_utils.drf_server.exceptions import BadRequest
from django_swagger_utils.utils.test import CustomAPITestCase

from display_reports.constants.general import DisplayReportStatus
from display_reports.utils.convert_unicode_strings import convert_unicode_strings
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
{
    "date_range": {
        "from_date": "2019-03-10", 
        "to_date": "2019-03-05"
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


class TestCase02GetDisplayReportsAPITestCase(CustomAPITestCase):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def test_case(self):
        self.default_test_case()
