from enum import Enum

from ib_common.constants import BaseEnumClass


class TournamentStatus(BaseEnumClass, Enum):
    CAN_JOIN = 'CAN_JOIN'
    FULL_YET_TO_START = 'FULL_YET_TO_START'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
