from django.db import models
from tournament.constants.general import USER_ID_MAX_LENGTH


class UserProfile(models.Model):
    user_id = models.CharField(max_length=USER_ID_MAX_LENGTH)
    name = models.CharField(max_length=30)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=10)

    @classmethod
    def create_user_profile(cls, user_id, name, age, gender):
        cls.objects.create(user_id=user_id, name=name, age=age, gender=gender)

    @classmethod
    def get_user(cls, user_id):
        return cls.objects.get(user_id=user_id)

    @classmethod
    def is_registered_user(cls, user_id):
        try:
            cls.get_user(user_id=user_id)
        except:
            from tournament.constants.exception_messages import \
                USER_NOT_REGISTERED
            raise Exception(*USER_NOT_REGISTERED)

    @classmethod
    def validate_users(cls, user_id_1, user_id_2):
        try:
            cls.get_user(user_id=user_id_1)
            cls.get_user(user_id=user_id_2)
        except:
            from tournament.constants.exception_messages import \
                USERS_OR_ONE_OF_THE_USER_NOT_REGISTERED
            raise Exception(*USERS_OR_ONE_OF_THE_USER_NOT_REGISTERED)
