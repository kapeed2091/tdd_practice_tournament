"""
# TODO: Update test case description
"""

from django_swagger_utils.utils.test import CustomAPITestCase
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

REQUEST_BODY = """
{
    "date_range": {
        "from_date": "2099-12-31", 
        "to_date": "2099-12-31"
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


class TestCase01SendDisplayReportsToFranchiseTeamAPITestCase(CustomAPITestCase):
    app_name = APP_NAME
    operation_name = OPERATION_NAME
    request_method = REQUEST_METHOD
    url_suffix = URL_SUFFIX
    test_case_dict = TEST_CASE

    def test_case(self):
        self.default_test_case() # Returns response object.
        # Which can be used for further response object checks.
        # Add database state checks here.