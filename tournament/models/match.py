from django.db import models

from tournament.constants.general import MatchStatus
from tournament.models import User
from tournament.models import KoTournament


class Match(models.Model):

    STATUS_LENGTH = 20

    user = models.ForeignKey(User)
    tournament = models.ForeignKey(KoTournament)
    status = models.CharField(max_length=STATUS_LENGTH)

    @classmethod
    def play_match(cls, user_id, match_id):
        match = cls.get_match(user_id=user_id, match_id=match_id)
        match.update_match_status(status=MatchStatus.IN_PROGRESS.value)

    @classmethod
    def get_match(cls, user_id, match_id):
        from tournament.models import User

        user = User.get_user(user_id)
        return cls.objects.get(user=user, id=match_id)

    def update_match_status(self, status):
        self.status = status
        self.save()
