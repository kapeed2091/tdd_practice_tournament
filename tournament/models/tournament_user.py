from django.db import models
from django_swagger_utils.drf_server.exceptions import Forbidden, BadRequest, NotFound

from tournament.constants.exception_messages import INVALID_USER_ID, INVALID_TOURNAMENT_ID, \
    ALREADY_SUBSCRIBED_TO_THIS_TOURNAMENT, SUBSCRIPTION_CAN_ONLY_BE_DONE_BEFORE_STARTING_OF_THE_TOURNAMENT, \
    THERE_IS_NO_PLACE_FOR_NEW_SUBSCRIPTION, USER_DOES_NOT_BELONG_TO_THE_TOURNAMENT
from tournament.models import User, KoTournament
from tournament.utils.date_time_utils import get_current_date_time


class TournamentUser(models.Model):

    user = models.ForeignKey(User)
    tournament = models.ForeignKey(KoTournament)

    @classmethod
    def get_tournament_user(cls, tournament, user):
        return cls.objects.get(tournament=tournament, user=user)

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        user = cls._get_user(user_id)
        tournament = cls._get_tournament(tournament_id)
        cls._validate_subscribe_request(tournament=tournament, user=user)
        cls._create_tournament_user(user=user, tournament=tournament)

    @classmethod
    def get_number_of_users(cls, tournament):
        return cls.objects.filter(tournament=tournament).count()

    @classmethod
    def validate_tournament_user(cls, user, tournament):
        try:
            cls.get_tournament_user(user=user, tournament=tournament)
        except cls.DoesNotExist:
            raise Forbidden(USER_DOES_NOT_BELONG_TO_THE_TOURNAMENT)

    @staticmethod
    def _get_user(user_id):
        from tournament.models import User
        try:
            return User.get_user(user_id)
        except NotFound:
            raise BadRequest(INVALID_USER_ID)

    @staticmethod
    def _get_tournament(tournament_id):
        from tournament.models import KoTournament
        try:
            return KoTournament.get_tournament(tournament_id)
        except NotFound:
            raise BadRequest(INVALID_TOURNAMENT_ID)

    @classmethod
    def _validate_subscribe_request(cls, tournament, user=user):
        cls._validate_weather_already_subscribed(tournament=tournament, user=user)
        cls._validate_tournament_start_datetime(tournament)
        cls._validate_max_members(tournament)

    @classmethod
    def _create_tournament_user(cls, user, tournament):
        cls.objects.create(user=user, tournament=tournament)

    @classmethod
    def _validate_weather_already_subscribed(cls, tournament, user):
        try:
            cls.get_tournament_user(tournament=tournament, user=user)
            raise BadRequest(ALREADY_SUBSCRIBED_TO_THIS_TOURNAMENT)
        except cls.DoesNotExist:
            pass

    @staticmethod
    def _validate_tournament_start_datetime(tournament):
        now = get_current_date_time()
        if tournament.start_datetime <= now:
            raise Forbidden(
                SUBSCRIPTION_CAN_ONLY_BE_DONE_BEFORE_STARTING_OF_THE_TOURNAMENT)

    @classmethod
    def _validate_max_members(cls, tournament):
        if tournament.has_max_members():
            raise Forbidden(THERE_IS_NO_PLACE_FOR_NEW_SUBSCRIPTION)
