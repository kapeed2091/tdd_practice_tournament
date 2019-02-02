from django.db import models


class Match(models.Model):
    user = models.ForeignKey('tournament.User')
    status = models.CharField(max_length=20, null=True)

    @classmethod
    def play_match(cls, match_id, user_id):
        match = cls.objects.get(id=match_id, user_id=user_id)
        match.status = "IN_PROGRESS"
        match.save()
