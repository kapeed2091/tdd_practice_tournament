from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=10, null=True)
    age = models.IntegerField(default=-1)

    @classmethod
    def validate_username(cls, username):
        if cls.is_username_does_not_exist(username):
            raise Exception("Invalid username")

    @classmethod
    def is_username_does_not_exist(cls, username):
        return not cls.objects.filter(username=username).exists()

    @classmethod
    def get_user_id(cls, username):
        try:
            return cls.objects.get(username=username).id
        except cls.DoesNotExist:
            raise Exception("Invalid user")

    @classmethod
    def get_user_profile(cls, user_id):
        user_obj = User.objects.get(id=user_id)

        return user_obj.get_user_profile_dict()

    def get_user_profile_dict(self):
        return {
            "user_id": self.id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age
            }