from django.db import models


class RoundMatch(models.Model):
    tournament = models.ForeignKey('tournament.Tournament')
    round_no = models.IntegerField()

    @classmethod
    def create_round_matches(cls, tournament_id):
        pass