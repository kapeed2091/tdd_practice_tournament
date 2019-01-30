from django.db import models
from django_swagger_utils.drf_server.exceptions import Forbidden

from tournament.models import User, KoTournament
from tournament.utils.date_time_utils import get_current_date_time


class TournamentUser(models.Model):

    user = models.ForeignKey(User)
    tournament = models.ForeignKey(KoTournament)

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from tournament.models import User, KoTournament

        user = User.get_user(user_id)
        tournament = KoTournament.get_tournament(tournament_id)
        cls.validate_tournament_start_datetime(tournament)
        cls.objects.create(user=user, tournament=tournament)

    @staticmethod
    def validate_tournament_start_datetime(tournament):
        now = get_current_date_time()
        if tournament.start_datetime <= now:
            raise Forbidden('Subscription can only be done before starting of the Tournament')
