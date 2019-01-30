from django.db import models


class UserTournament(models.Model):
    user_id = models.PositiveIntegerField()
    tournament_id = models.PositiveIntegerField()

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from ..models import Tournament
        Tournament.validate_tournament_id(tournament_id=tournament_id)

        cls.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
        )
