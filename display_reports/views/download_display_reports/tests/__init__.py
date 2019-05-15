# pylint: disable=wrong-import-position

APP_NAME = "display_reports"
OPERATION_NAME = "download_display_reports"
REQUEST_METHOD = "post"
URL_SUFFIX = "download/display_reports/v1/"

from .test_case_01 import TestCase01DownloadDisplayReportsAPITestCase

__all__ = [
    "TestCase01DownloadDisplayReportsAPITestCase"
]
