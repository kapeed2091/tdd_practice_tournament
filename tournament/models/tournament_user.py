from django.db import models


class TournamentUser(models.Model):
    user = models.ForeignKey('tournament.User')
    tournament = models.ForeignKey('tournament.Tournament')

    @classmethod
    def subscribe_user_to_tournament(cls, tournament_id, username):
        from .user import User
        cls.validate_user_already_subscribed(
            tournament_id=tournament_id, username=username)
        user_id = User.get_user_id(username=username)

        cls.objects.create(user_id=user_id, tournament_id=tournament_id)

    @classmethod
    def validate_user_already_subscribed(cls, tournament_id, username):
        try:
            cls.objects.get(tournament_id=tournament_id, user__username=username)
            raise Exception("User already subscribed to given tournament")
        except cls.DoesNotExist:
            pass
