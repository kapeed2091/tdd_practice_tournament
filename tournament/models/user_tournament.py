from django.db import models


class UserTournament(models.Model):
    user_id = models.PositiveIntegerField()
    tournament_id = models.PositiveIntegerField()

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from ..models import Tournament
        tournament_exists = Tournament.objects.filter(
            id=tournament_id).exists()

        if not tournament_exists:
            from ..exceptions.exceptions import InvalidTournamentId
            raise InvalidTournamentId

        cls.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
        )
