from django.db import models


class TournamentUser(models.Model):
    user = models.ForeignKey('tournament.User')
    tournament = models.ForeignKey('tournament.Tournament')

    @classmethod
    def subscribe_user_to_tournament(cls, tournament_id, username):
        from .user import User
        user_id = User.get_user_id(username=username)

        cls.objects.create(user_id=user_id, tournament_id=tournament_id)
