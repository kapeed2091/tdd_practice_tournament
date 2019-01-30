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
    def get_player_by_id(cls, player_id):
        try:
            player = cls.objects.get(id=player_id)
            return player
        except cls.DoesNotExist:
            from django_swagger_utils.drf_server.exceptions import BadRequest
            from ib_tournament.constants.exception_messages import INVALID_USER
            raise BadRequest(*INVALID_USER)
        return

    @classmethod
    def _validate_unique_username(cls, username):
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import USERNAME_EXISTS
        if Player.objects.filter(username=username):
            raise BadRequest(USERNAME_EXISTS)
        return
