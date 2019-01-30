from django.db import models
from tournament.constants.general import T_ID_MAX_LENGTH, USER_ID_MAX_LENGTH


class TournamentUser(models.Model):
    user_id = models.CharField(max_length=T_ID_MAX_LENGTH)
    t_id = models.CharField(max_length=USER_ID_MAX_LENGTH)

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from tournament.models import UserProfile, KOTournament

        UserProfile.is_registered_user(user_id=user_id)
        KOTournament.is_tournament_exists(tournament_id=tournament_id)
        tournament_obj = KOTournament.get_tournament(tournament_id=tournament_id)
        KOTournament.is_tournament_started(tournament_obj=tournament_obj)

        cls.create_tournamentuser(user_id=user_id, tournament_id=tournament_id)

    @classmethod
    def create_tournamentuser(cls, user_id, tournament_id):
        cls.objects.create(user_id=user_id, t_id=tournament_id)
