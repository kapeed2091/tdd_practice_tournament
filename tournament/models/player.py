from django.db import models


class Player(models.Model):
    username = models.CharField(max_length=50)

    @classmethod
    def create_player(cls, username):
        cls.objects.create(username=username)

    @classmethod
    def get_player_dict(cls, username):
        player = cls.objects.get(username=username)
        return {
            'username': player.username
        }
