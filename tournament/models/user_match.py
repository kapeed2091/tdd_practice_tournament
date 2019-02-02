from django.db import models


class UserMatch(models.Model):
    user_id = models.PositiveIntegerField()
    match_id = models.PositiveIntegerField()

    @classmethod
    def create_user_match(cls, user_id, match_id):
        cls.objects.create(
            user_id=user_id,
            match_id=match_id
        )
