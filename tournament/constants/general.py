from enum import Enum
from ib_common.constants import BaseEnumClass


class TournamentStatus(BaseEnumClass, Enum):
    CAN_JOIN = 'CAN_JOIN'
    FULL_YET_TO_START = 'FULL_YET_TO_START'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class PlayerMatchStatus(BaseEnumClass, Enum):
    YET_TO_START = 'YET_TO_START'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class MatchStatus(BaseEnumClass, Enum):
    YET_TO_START = 'YET_TO_START'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


T_ID_MAX_LENGTH = 20
USER_ID_MAX_LENGTH = 20
