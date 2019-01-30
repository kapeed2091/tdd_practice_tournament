from django.db import models


class TournamentUser(models.Model):

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        pass
