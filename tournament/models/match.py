from django.db import models
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
        pass
