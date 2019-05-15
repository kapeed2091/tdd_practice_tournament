# pylint: disable=wrong-import-position

APP_NAME = "display_reports"
OPERATION_NAME = "send_display_reports_to_franchise_team"
REQUEST_METHOD = "post"
URL_SUFFIX = "send/display_reports/franchise_team/v1/"

from .test_case_01 import TestCase01SendDisplayReportsToFranchiseTeamAPITestCase

__all__ = [
    "TestCase01SendDisplayReportsToFranchiseTeamAPITestCase"
]
