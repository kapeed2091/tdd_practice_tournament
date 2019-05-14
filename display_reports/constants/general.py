from enum import Enum
from ib_common.constants import BaseEnumClass


class TransactionStatus(BaseEnumClass, Enum):
    SUCCESS = "SUCCESS"


class DisplayReportStatus(BaseEnumClass, Enum):
    MATCHED = "MATCHED"
    AMOUNT_MISMATCH = "AMOUNT_MISMATCH"
