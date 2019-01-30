from django.db import models


class TournamentPlayer(models.Model):
    tournament = models.ForeignKey('ib_tournament.Tournament')
    player = models.ForeignKey('ib_tournament.Player')

    class Meta:
        unique_together = ('tournament', 'player')

    @classmethod
    def get_tournament_player(cls, tournament_id, player_id):
        return cls.objects.get(tournament_id=tournament_id, player_id=player_id)

    def get_tournament_player_dict(self):
        return {
            'tournament_id': self.tournament_id,
            'player_id': self.player_id
        }

    @classmethod
    def create_tournament_player(cls, tournament_id, player_id):
        cls.objects.create(tournament_id=tournament_id, player_id=player_id)

    @classmethod
    def get_tournament_player_exists(cls, tournament_id, player_id):
        return cls.objects.filter(
            tournament_id=tournament_id, player_id=player_id).exists()
