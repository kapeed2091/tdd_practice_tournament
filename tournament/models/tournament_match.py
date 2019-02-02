from django.db import models
from tournament.constants.general import T_ID_MAX_LENGTH,USER_ID_MAX_LENGTH


class TournamentMatch(models.Model):
    t_id = models.CharField(max_length=T_ID_MAX_LENGTH)
    player_one = models.CharField(max_length=USER_ID_MAX_LENGTH)
    player_two = models.CharField(max_length=USER_ID_MAX_LENGTH)

    @classmethod
    def create_match(cls, request_data):
        from tournament.models import KOTournament
        KOTournament.is_tournament_exists(
            tournament_id=request_data['tournament_id'])
        KOTournament.validate_start_datetime(
            tournament_id=request_data['tournament_id'])
        cls.objects.create(
            t_id=request_data['tournament_id'],
            player_one=request_data['player_one_user_id'],
            player_two=request_data['player_two_user_id'])
