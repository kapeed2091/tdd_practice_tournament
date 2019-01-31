from django.db import models
from tournament.models import User
from tournament.models import KoTournament


class Match(models.Model):

    STATUS_LENGTH = 20

    user = models.ForeignKey(User)
    tournament = models.ForeignKey(KoTournament)
    status = models.CharField(max_length=STATUS_LENGTH)

    @classmethod
    def play_match(cls, user_id, match_id):
        pass
