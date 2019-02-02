from django.db import models


class TMPlayer(models.Model):
    player_id = models.IntegerField()
    tournament_match_id = models.IntegerField()

    @classmethod
    def add_players_to_matches(cls, tournament_id):
        pass
