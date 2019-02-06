from django.db import models
from tournament.constants.general import T_ID_MAX_LENGTH, USER_ID_MAX_LENGTH


class TournamentUser(models.Model):
    user_id = models.CharField(max_length=T_ID_MAX_LENGTH)
    t_id = models.CharField(max_length=USER_ID_MAX_LENGTH)
    current_round_number = models.IntegerField(default=1)

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from tournament.models import UserProfile, KOTournament

        cls.is_tournament_user_exists(user_id=user_id,
                                      tournament_id=tournament_id)
        UserProfile.is_registered_user(user_id=user_id)
        KOTournament.validate_subscribe_request(tournament_id=tournament_id)

        max_users_count = KOTournament.get_max_users_count(
            tournament_id=tournament_id)
        subscribed_users_count = cls.get_subscribed_users_count(
            tournament_id=tournament_id)

        cls.is_tournament_full(subscribed_users_count=subscribed_users_count,
                               max_users_count=max_users_count)
        cls.create_tournamentuser(user_id=user_id, tournament_id=tournament_id)
        cls.change_tournament_status_to_full(
            subscribed_users_count=subscribed_users_count,
            max_users_count=max_users_count, tournament_id=tournament_id)

    @classmethod
    def create_tournamentuser(cls, user_id, tournament_id):
        cls.objects.create(user_id=user_id, t_id=tournament_id)

    @classmethod
    def is_tournament_user_exists(cls, user_id, tournament_id):
        if len(cls.objects.filter(user_id=user_id, t_id=tournament_id)) > 0:
            raise Exception('Already Subscribed to Tournament')

    @classmethod
    def get_subscribed_users_count(cls, tournament_id):
        return len(cls.objects.filter(t_id=tournament_id))

    @staticmethod
    def is_tournament_full(subscribed_users_count, max_users_count):
        if subscribed_users_count == max_users_count:
            raise Exception('Tournament is full')

    @classmethod
    def change_tournament_status_to_full(cls, subscribed_users_count,
                                         max_users_count, tournament_id):
        if cls.is_last_subscriber(subscribed_users_count=subscribed_users_count,
                                  max_users_count=max_users_count):
            from tournament.models import KOTournament
            KOTournament.change_tournament_status_to_full(
                tournament_id=tournament_id)

    @staticmethod
    def is_last_subscriber(subscribed_users_count, max_users_count):
        if max_users_count - subscribed_users_count == 1:
            return True
        else:
            return False

    @classmethod
    def validate_users_subscription(cls, tournament_id, user_id_1, user_id_2):
        try:
            cls.objects.get(t_id=tournament_id, user_id=user_id_1)
            cls.objects.get(t_id=tournament_id, user_id=user_id_2)
        except:
            from tournament.constants.exception_messages import \
                USERS_OR_ONE_OF_THE_USER_NOT_SUBSCRIBED_TO_TOURNAMENT
            raise Exception(
                *USERS_OR_ONE_OF_THE_USER_NOT_SUBSCRIBED_TO_TOURNAMENT)

    @classmethod
    def validate_user_subscription(cls, tournament_id, user_id):
        try:
            cls.objects.get(t_id=tournament_id, user_id=user_id)
        except:
            from tournament.constants.exception_messages import \
                USER_NOT_SUBSCRIBED_TO_TOURNAMENT
            raise Exception(
                *USER_NOT_SUBSCRIBED_TO_TOURNAMENT)
