from enum import Enum

DEFAULT_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TournamentStatus(Enum):
    CAN_JOIN = 'CAN_JOIN'
    FULL_YET_TO_START = 'FULL_YET_TO_START'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
