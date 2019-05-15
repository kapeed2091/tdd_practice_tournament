from enum import Enum
from ib_common.constants import BaseEnumClass


class TransactionStatus(BaseEnumClass, Enum):
    SUCCESS = "SUCCESS"


class DisplayReportStatus(BaseEnumClass, Enum):
    MATCHED = "MATCHED"
    AMOUNT_MISMATCH = "AMOUNT_MISMATCH"
    REF_NO_MISMATCH = "REF_NO_MISMATCH"
    EXTRA_SALE = "EXTRA_SALE"
    UN_BILLED = "UN_BILLED"


PAYMENT_REPORT_TRANSACTION_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
