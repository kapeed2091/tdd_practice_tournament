from django.db import models
from tournament.constants.general import USER_ID_MAX_LENGTH


class UserProfile(models.Model):
    user_id = models.CharField(max_length=USER_ID_MAX_LENGTH)

    @classmethod
    def get_user(cls, user_id):
        return cls.objects.get(user_id=user_id)

    @classmethod
    def is_registered_user(cls, user_id):
        try:
            cls.get_user(user_id=user_id)
        except:
            raise Exception('User not registered')
