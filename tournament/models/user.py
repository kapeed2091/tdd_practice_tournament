from django.db import models


class User(models.Model):
    USER_ID_LENGTH = 20

    user_id = models.CharField(max_length=USER_ID_LENGTH)

    @classmethod
    def get_user(cls, user_id):
        return cls.objects.get(user_id=user_id)
