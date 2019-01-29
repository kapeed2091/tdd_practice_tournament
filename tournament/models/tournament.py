from django.db import models


class Tournament(models.Model):
    user_id = models.PositiveIntegerField()
    total_rounds = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()

    @classmethod
    def create_tournament(cls, user_id, total_rounds, start_datetime):

        from .user import User
        user_exists = User.objects.filter(id=user_id).exists()
        if not user_exists:
            from ..exceptions.exceptions import InvalidUserId
            raise InvalidUserId

        obj = Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime
        )
        return obj
