from enum import Enum
from ib_common.constants.base_enum_class import BaseEnumClass


class TournamentStatus(BaseEnumClass, Enum):
    NOT_YET_STARTED = 'NOT_YET_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
