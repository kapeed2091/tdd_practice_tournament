from django.db import models


class TournamentUser(models.Model):
    user = models.ForeignKey('tournament.User')
    tournament = models.ForeignKey('tournament.Tournament')

    @classmethod
    def subscribe_user_to_tournament(cls, tournament_id, username):
        pass
