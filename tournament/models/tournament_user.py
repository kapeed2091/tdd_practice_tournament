from django.db import models
from tournament.models import User, KoTournament


class TournamentUser(models.Model):

    user = models.ForeignKey(User)
    tournament = models.ForeignKey(KoTournament)

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from tournament.models import User, KoTournament

        user = User.get_user(user_id)
        tournament = KoTournament.get_tournament(tournament_id)
        cls.objects.create(user=user, tournament=tournament)

