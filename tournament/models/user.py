from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)

    @classmethod
    def validate_username(cls, username):
        if cls.is_username_does_not_exist(username):
            raise Exception("Invalid username")

    @classmethod
    def is_username_does_not_exist(cls, username):
        return not cls.objects.filter(username=username).exists()

    @classmethod
    def get_user_id(cls, username):
        return cls.objects.get(username=username).id
