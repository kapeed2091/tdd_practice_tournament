from django.db import models


class TournamentUser(models.Model):
    user_id = models.CharField(max_length=20)
    tournament_id = models.CharField(max_length=20)

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        try:
            from tournament.models import UserProfile
            UserProfile.get_user(user_id=user_id)
        except:
            raise Exception('User not registered')

        cls.objects.create(user_id=user_id, tournament_id=tournament_id)