from django.db import models


class TournamentMatch(models.Model):
    t_id = models.CharField(max_length=20)
    player_one = models.CharField(max_length=20)
    player_two = models.CharField(max_length=20)

    @classmethod
    def create_match(cls, tournament_id, user_id_1, user_id_2):
        pass