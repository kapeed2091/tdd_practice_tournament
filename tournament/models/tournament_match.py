from django.db import models


class TournamentMatch(models.Model):
    tournament = models.ForeignKey('tournament.Tournament')
    round_no = models.IntegerField()
    match_id = models.CharField(max_length=50)

