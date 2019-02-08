from django.db import models
from django_swagger_utils.drf_server.exceptions import NotFound

from tournament.constants.exception_messages import USER_DOES_NOT_EXIST_WITH_THE_GIVEN_USER_ID


class User(models.Model):
    USER_ID_LENGTH = 20
    NAME_LENGTH = 20
    GENDER_LENGTH = 10

    user_id = models.CharField(max_length=USER_ID_LENGTH)
    name = models.CharField(max_length=NAME_LENGTH)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=GENDER_LENGTH)

    @classmethod
    def get_user(cls, user_id):
        try:
            return cls.objects.get(user_id=user_id)
        except cls.DoesNotExist:
            raise NotFound(USER_DOES_NOT_EXIST_WITH_THE_GIVEN_USER_ID)

    def convert_to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
