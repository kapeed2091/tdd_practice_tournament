from django.db import models


class TournamentPlayer(models.Model):
    pass

    @classmethod
    def get_tournament_player(cls, tournament_id, player_id):
        return TournamentPlayer()

    def get_tournament_player_dict(self):
        return {
            'tournament_id': -1,
            'player_id': ''
        }
