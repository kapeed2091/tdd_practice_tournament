from django.db import models
from django_swagger_utils.drf_server.exceptions import Forbidden, NotFound

from tournament.constants.exception_messages import MATCH_CAN_BE_PLAYED_ONLY_AFTER_THE_TOURNAMENT_HAS_STARTED, \
    USER_DOES_NOT_EXIST_WITH_THE_GIVEN_USER_ID, USER_DOES_NOT_BELONG_TO_THE_MATCH, \
    MATCH_DOES_NOT_EXIST_WITH_THE_GIVEN_MATCH_ID
from tournament.constants.general import MatchStatus
from tournament.models import User, KoTournament


class Match(models.Model):
    MATCH_ID_LENGTH = 20
    STATUS_LENGTH = 20

    match_id = models.CharField(max_length=MATCH_ID_LENGTH)
    user = models.ForeignKey(User)
    tournament = models.ForeignKey(KoTournament)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=STATUS_LENGTH)

    @classmethod
    def play_match(cls, user_id, match_id):
        user = cls._get_user(user_id)
        cls._validate_match(match_id)
        match = cls._get_match(user=user, match_id=match_id)
        cls._validate_tournament(tournament=match.tournament)
        match.update_status(status=MatchStatus.IN_PROGRESS.value)

    def update_status(self, status):
        self.status = status
        self.save()

    @staticmethod
    def _get_user(user_id):
        from tournament.models import User

        try:
            return User.get_user(user_id)
        except User.DoesNotExist:
            raise NotFound(USER_DOES_NOT_EXIST_WITH_THE_GIVEN_USER_ID)

    @staticmethod
    def _validate_tournament(tournament):
        if tournament.is_not_started():
            raise Forbidden(MATCH_CAN_BE_PLAYED_ONLY_AFTER_THE_TOURNAMENT_HAS_STARTED)

    @classmethod
    def _get_match(cls, user, match_id):
        try:
            return cls.objects.get(user=user, match_id=match_id)
        except cls.DoesNotExist:
            raise Forbidden(USER_DOES_NOT_BELONG_TO_THE_MATCH)

    @classmethod
    def _validate_match(cls, match_id):
        if cls._does_not_match_exists(match_id):
            raise NotFound(MATCH_DOES_NOT_EXIST_WITH_THE_GIVEN_MATCH_ID)

    @classmethod
    def _does_not_match_exists(cls, match_id):
        return not cls._does_match_exists(match_id)

    @classmethod
    def _does_match_exists(cls, match_id):
        return cls.objects.filter(match_id=match_id).exists()
