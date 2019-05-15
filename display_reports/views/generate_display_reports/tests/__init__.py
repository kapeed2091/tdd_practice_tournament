# pylint: disable=wrong-import-position

APP_NAME = "display_reports"
OPERATION_NAME = "generate_display_reports"
REQUEST_METHOD = "post"
URL_SUFFIX = "generate/display_reports/v1/"

from .test_case_01 import TestCase01GenerateDisplayReportsAPITestCase

__all__ = [
    "TestCase01GenerateDisplayReportsAPITestCase"
]
