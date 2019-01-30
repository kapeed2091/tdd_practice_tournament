from django.db import models
from tournament.constants.general import T_ID_MAX_LENGTH, USER_ID_MAX_LENGTH


class TournamentUser(models.Model):
    user_id = models.CharField(max_length=T_ID_MAX_LENGTH)
    t_id = models.CharField(max_length=USER_ID_MAX_LENGTH)

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from tournament.models import UserProfile, KOTournament

        if len(cls.objects.filter(user_id=user_id, t_id=tournament_id)) > 0:
            raise Exception('Already Subscribed to Tournament')

        UserProfile.is_registered_user(user_id=user_id)
        KOTournament.is_tournament_exists(tournament_id=tournament_id)
        tournament_obj = KOTournament.get_tournament(tournament_id=tournament_id)
        KOTournament.is_tournament_started(tournament_obj=tournament_obj)

        max_participants = KOTournament.get_max_participants_count(
            tournament_obj=tournament_obj)
        subscribed_participants = len(cls.objects.filter(t_id=tournament_id))
        if subscribed_participants == max_participants:
            raise Exception('Tournament is full')

        KOTournament.is_valid_subscribe_status(tournament_obj=tournament_obj)

        cls.create_tournamentuser(user_id=user_id, tournament_id=tournament_id)
        if max_participants - subscribed_participants == 1:
            KOTournament.change_tournament_status_to_full(
                tournament_obj=tournament_obj)

    @classmethod
    def create_tournamentuser(cls, user_id, tournament_id):
        cls.objects.create(user_id=user_id, t_id=tournament_id)
