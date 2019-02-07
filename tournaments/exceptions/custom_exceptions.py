class InvalidUserId(Exception):
    pass


class InvalidStartDateTime(Exception):
    pass


class InvalidTotalRounds(Exception):
    pass


class InvalidTournamentId(Exception):
    pass


class UserAlreadyRegistered(Exception):
    pass


class InvalidFullYetToStartRegister(Exception):
    pass


class InvalidInProgresstRegister(Exception):
    pass


class InvalidCompletedRegister(Exception):
    pass


class UserNotInTournament(Exception):
    pass


class InvalidRoundNumber(Exception):
    pass


class InvalidMatchId(Exception):
    pass


class InvalidScore(Exception):
    pass


class ScoreCannotBeUpdated(Exception):
    pass


class MatchIdOverused(Exception):
    pass


class UserNotInTournamentAnymore(Exception):
    pass


class UserAlreadyLeveledUp(Exception):
    pass


class UserNotInMatch(Exception):
    pass


class UserDidNotWinMatch(Exception):
    pass


class TournamentMatchesAlreadyExist(Exception):
    pass


class InsufficientMembersInRound(Exception):
    pass


class InadequateNumberOfMatches(Exception):
    pass


class ReAssignmentOfPlayers(Exception):
    pass


class RoundNumberOutOfBounds(Exception):
    pass


class OpponentNotYetAssigned(Exception):
    pass


class TournamentInProgress(Exception):
    pass


class TournamentNotYetStarted(Exception):
    pass


class LoserStatusAlreadyUpdated(Exception):
    pass
