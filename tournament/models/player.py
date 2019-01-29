from django.db import models


class Player(models.Model):
    username = models.CharField(max_length=50)

    @classmethod
    def create_player(cls, username):
        cls.objects.create(username=username)

    @classmethod
    def get_player(cls, username):
        return cls.objects.get(username=username)

    def get_player_dict(self):
        return {
            'username': self.username
        }
