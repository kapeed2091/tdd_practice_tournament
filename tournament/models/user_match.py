from django.db import models


class UserMatch(models.Model):
    user_id = models.PositiveIntegerField()
    match_id = models.PositiveIntegerField()

    @classmethod
    def create_user_match(cls, user_id, match_id):
        from .match import Match
        match_exists = Match.objects.filter(id=match_id).exists()

        if not match_exists:
            from ..exceptions.custom_exceptions import InvalidMatchId
            raise InvalidMatchId

        cls.objects.create(
            user_id=user_id,
            match_id=match_id
        )
