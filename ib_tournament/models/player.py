from django.db import models


class Player(models.Model):
    username = models.CharField(max_length=50, unique=True)

    @classmethod
    def create_player(cls, username):
        cls._validate_unique_username(username)
        cls.objects.create(username=username)
        return

    @classmethod
    def get_player(cls, username):
        return cls.objects.get(username=username)

    def get_player_dict(self):
        return {
            'username': self.username
        }

    @classmethod
    def _validate_unique_username(cls, username):
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import USERNAME_EXISTS
        if Player.objects.filter(username=username):
            raise BadRequest(USERNAME_EXISTS)
        return
