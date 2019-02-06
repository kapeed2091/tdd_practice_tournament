from django.db import models


class User(models.Model):
    NAME_MAX_LENGTH = 20
    GENDER_MAX_LENGTH = 20

    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=GENDER_MAX_LENGTH)

    @classmethod
    def validate_user_id(cls, user_id):
        user_exists = User.objects.filter(id=user_id).exists()
        if not user_exists:
            from ..exceptions.custom_exceptions import InvalidUserId
            raise InvalidUserId
