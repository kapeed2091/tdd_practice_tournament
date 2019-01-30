from django.db import models


class TournamentUser(models.Model):
    user_id = models.CharField(max_length=20)
    tournament_id = models.CharField(max_length=20)

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from tournament.models import UserProfile
        UserProfile.is_registered_user(user_id=user_id)

        cls.objects.create(user_id=user_id, tournament_id=tournament_id)