from django.db import models
from django_swagger_utils.drf_server.exceptions import Forbidden

from tournament.constants.exception_messages import MATCH_CAN_BE_PLAYED_ONLY_AFTER_THE_TOURNAMENT_HAS_STARTED
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
        from tournament.models import User

        user = User.get_user(user_id)
        match = cls._get_match(user=user, match_id=match_id)
        cls._validate_tournament(tournament=match.tournament)
        match.update_status(status=MatchStatus.IN_PROGRESS.value)

    @staticmethod
    def _validate_tournament(tournament):
        if tournament.is_not_started():
            raise Forbidden(MATCH_CAN_BE_PLAYED_ONLY_AFTER_THE_TOURNAMENT_HAS_STARTED)

    @classmethod
    def _get_match(cls, user, match_id):
        return cls.objects.get(user=user, match_id=match_id)

    def update_status(self, status):
        self.status = status
        self.save()
