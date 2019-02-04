from enum import Enum


class TournamentStatus(Enum):
    YET_TO_START = "YET_TO_START"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class MatchStatus(Enum):
    YET_TO_START = "YET_TO_START"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class MatchUserStatus(Enum):
    NOT_DECIDED_YET = 'NOT_DECIDED_YET'
    WIN = 'WIN'
    LOST = 'LOST'
