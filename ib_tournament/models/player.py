from django.db import models


class Player(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)

    @classmethod
    def create_player(cls, user_details):
        cls._validate_unique_username(user_details['username'])
        cls.objects.create(
            username=user_details['username'], name=user_details['name'],
            age=user_details['age'], gender=user_details['gender'])
        return

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
    def get_player_profile_by_id(cls, player_id):
        player = cls.get_player_by_id(player_id)
        return cls._get_player_profile(player)

    @classmethod
    def _validate_unique_username(cls, username):
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import USERNAME_EXISTS
        if cls.objects.filter(username=username):
            raise BadRequest(USERNAME_EXISTS)
        return

    def _get_player_profile(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
