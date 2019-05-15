# pylint: disable=wrong-import-position

APP_NAME = "display_reports"
OPERATION_NAME = "upload_payment_reports"
REQUEST_METHOD = "post"
URL_SUFFIX = "upload/payment_reports/v1/"

from .test_case_01 import TestCase01UploadPaymentReportsAPITestCase

__all__ = [
    "TestCase01UploadPaymentReportsAPITestCase"
]
