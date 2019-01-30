from django.db import models


class UserTournament(models.Model):
    user_id = models.PositiveIntegerField()
    tournament_id = models.PositiveIntegerField()

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from ..models import User, Tournament
        Tournament.validate_tournament_id(tournament_id=tournament_id)

        user_exists = User.objects.filter(id=user_id).exists()
        if not user_exists:
            from ..exceptions.exceptions import InvalidUserId
            raise InvalidUserId

        cls.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
        )
