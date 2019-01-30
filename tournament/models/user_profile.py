from django.db import models


class UserProfile(models.Model):
    user_id = models.CharField(max_length=20)

    @classmethod
    def get_user(cls, user_id):
        return cls.objects.get(user_id=user_id)
