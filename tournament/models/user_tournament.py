from django.db import models


class UserTournament(models.Model):

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        pass
