from django.db import models


class UserTournament(models.Model):
    user_id = models.PositiveIntegerField()
    tournament_id = models.PositiveIntegerField()

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from ..models import User, Tournament

        Tournament.validate_tournament_id(tournament_id=tournament_id)

        User.validate_user_id(user_id=user_id)

        user_tournament_exists = cls.objects.filter(
            user_id=user_id, tournament_id=tournament_id
        )

        if user_tournament_exists:
            from ..exceptions.exceptions import UserAlreadyRegistered
            raise UserAlreadyRegistered

        cls.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
        )
