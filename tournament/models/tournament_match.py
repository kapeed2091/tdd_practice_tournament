from django.db import models
from tournament.constants.general import T_ID_MAX_LENGTH,USER_ID_MAX_LENGTH


class TournamentMatch(models.Model):
    t_id = models.CharField(max_length=T_ID_MAX_LENGTH)
    player_one = models.CharField(max_length=USER_ID_MAX_LENGTH)
    player_two = models.CharField(max_length=USER_ID_MAX_LENGTH)
    match_id = models.CharField(max_length=20)

    @classmethod
    def create_match(cls, request_data):
        from tournament.models import KOTournament, UserProfile, TournamentUser
        KOTournament.validate_tournament_for_create_match(
            tournament_id=request_data['tournament_id'])
        UserProfile.validate_users(user_id_1=request_data['player_one_user_id'],
                                   user_id_2=request_data['player_two_user_id'])
        TournamentUser.validate_users_subscription(
            tournament_id=request_data['tournament_id'],
            user_id_1=request_data['player_one_user_id'],
            user_id_2=request_data['player_two_user_id'])
        cls.objects.create(
            t_id=request_data['tournament_id'],
            player_one=request_data['player_one_user_id'],
            player_two=request_data['player_two_user_id'])

    @classmethod
    def assign_match_id(cls, request_data, match_id):
        if cls.objects.filter(match_id=match_id).exists():
            raise Exception('Match id already assigned to another match')
        else:
            cls.objects.create(
                t_id=request_data['tournament_id'],
                player_one=request_data['player_one_user_id'],
                player_two=request_data['player_two_user_id'],
                match_id=match_id)
