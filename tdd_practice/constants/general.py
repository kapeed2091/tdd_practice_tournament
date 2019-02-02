"""
Created on 28/05/18

@author: revanth
"""

from enum import Enum
from ib_common.constants.base_enum_class import BaseEnumClass

DEFAULT_PASSWORD = 'iBC@2091'

DEFAULT_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE_TIME_FORMAT_WITHOUT_SEC = '%Y-%m-%d %H:%M'
DEFAULT_DATE_TIME_FORMAT_WITH_MICROSEC = '%Y-%m-%d %H:%M:%S.%f'

DEFAULT_DATE_FORMAT = '%Y-%m-%d'

DEFAULT_TIME_FORMAT = '%H:%M'


class TournamentStatus(Enum):
    CAN_JOIN = "CAN_JOIN"
    FULL_YET_TO_START = "FULL_YET_TO_START"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class UserMatchStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"

