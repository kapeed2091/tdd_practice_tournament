# pylint: disable=wrong-import-position

APP_NAME = "display_reports"
OPERATION_NAME = "get_display_reports"
REQUEST_METHOD = "post"
URL_SUFFIX = "get/display_reports/v1/"

from .test_case_01 import TestCase01GetDisplayReportsAPITestCase

__all__ = [
    "TestCase01GetDisplayReportsAPITestCase"
]
