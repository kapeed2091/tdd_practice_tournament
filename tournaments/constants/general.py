from enum import Enum

from ib_common.constants import BaseEnumClass


class TournamentStatus(BaseEnumClass, Enum):
    CAN_JOIN = 'CAN_JOIN'
    FULL_YET_TO_START = 'FULL_YET_TO_START'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class UserTournamentStatus(BaseEnumClass, Enum):
    ALIVE = "ALIVE"
    DEAD = "DEAD"


DEFAULT_SCORE = -1

MAX_NUM_OF_PEOPLE_FOR_MATCH = 2

DEFAULT_USER_TOURNAMENT_ROUND_NUMBER = 0
