from django.db import models


class Match(models.Model):
    user = models.ForeignKey('tournament.User')
    tournament = models.ForeignKey('tournament.Tournament', null=True)
    status = models.CharField(max_length=20, null=True)

    @classmethod
    def play_match(cls, match_id, user_id):
        from tdd_practice.constants.general import UserMatchStatus

        match = cls.objects.get(id=match_id, user_id=user_id)
        match.update_match_status(status=UserMatchStatus.IN_PROGRESS.value)

    def update_match_status(self, status):
        self.status = status
        self.save()

    @classmethod
    def get_tournament_by_match_id(cls, match_id):
        return
