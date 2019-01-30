from django.db import models
from django_swagger_utils.drf_server.exceptions import Forbidden, BadRequest

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
        from tournament.models import User, KoTournament

        user = User.get_user(user_id)
        tournament = KoTournament.get_tournament(tournament_id)
        cls._validate_subscribe_request(tournament=tournament, user=user)
        cls.objects.create(user=user, tournament=tournament)

    @classmethod
    def _validate_subscribe_request(cls, tournament, user=user):
        cls._validate_weather_already_subscribed(tournament=tournament, user=user)
        cls._validate_tournament_start_datetime(tournament)
        cls._validate_max_members(tournament)

    @classmethod
    def _validate_weather_already_subscribed(cls, tournament, user):
        try:
            cls.get_tournament_user(tournament=tournament, user=user)
            raise BadRequest('Already subscribed to this tournament')
        except cls.DoesNotExist:
            pass

    @staticmethod
    def _validate_tournament_start_datetime(tournament):
        now = get_current_date_time()
        if tournament.start_datetime <= now:
            raise Forbidden('Subscription can only be done before starting of the Tournament')

    @classmethod
    def _validate_max_members(cls, tournament):
        no_of_rounds = tournament.no_of_rounds
        max_members_allowed = 2 ** no_of_rounds

        no_of_users = cls.objects.filter(tournament=tournament).count()
        if no_of_users == max_members_allowed:
            raise Forbidden('There is no place for new subscriptions')
