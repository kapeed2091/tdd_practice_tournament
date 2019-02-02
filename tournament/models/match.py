from django.db import models


class Match(models.Model):
    user = models.ForeignKey('tournament.User')
    tournament = models.ForeignKey('tournament.Tournament', null=True)
    status = models.CharField(max_length=20, null=True)
    score = models.IntegerField(default=-1)

    @classmethod
    def play_match(cls, match_id, user_id):
        from tdd_practice.constants.general import UserMatchStatus

        match = cls.get_match(match_id=match_id, user_id=user_id)
        match.validate_play_match()

        match.update_match_status(status=UserMatchStatus.IN_PROGRESS.value)

    @classmethod
    def get_tournament_by_match_id(cls, match_id):
        match = cls.objects.get(id=match_id)
        return match.tournament

    def validate_play_match(self):
        if self.tournament.is_tournament_not_started():
            raise Exception("User can not play match until match is started")

    @classmethod
    def user_submit_match_score(cls, user_match_score):
        from tdd_practice.constants.general import UserMatchStatus

        score = user_match_score['score']
        match_id = user_match_score['match_id']
        user_id = user_match_score['user_id']

        match = cls.get_match(match_id=match_id, user_id=user_id)
        match.update_match_score(score=score)
        match.update_match_status(status=UserMatchStatus.COMPLETED.value)

    @classmethod
    def get_match(cls, match_id, user_id):
        return cls.objects.get(id=match_id, user_id=user_id)

    def update_match_status(self, status):
        self.status = status
        self.save()

    def update_match_score(self, score):
        self.score = score
        self.save()
