from django.db import models


class Match(models.Model):
    user = models.ForeignKey('tournament.User')
    tournament = models.ForeignKey('tournament.Tournament', null=True)
    status = models.CharField(max_length=20, null=True)
    score = models.IntegerField(default=-1)
    score_submission_datetime = models.DateTimeField(null=True)
    round_match = models.ForeignKey('tournament.RoundMatch')

    @classmethod
    def play_match(cls, match_id, user_id):
        from tdd_practice.constants.general import UserMatchStatus
        cls._validate_user_match(match_id, user_id)
        match = cls.get_match(round_match_id=match_id, user_id=user_id)
        match.validate_play_match()

        match.update_status(status=UserMatchStatus.IN_PROGRESS.value)

    @classmethod
    def get_user_current_round_no(cls, tournament_id, user_id):
        round_nos = list(Match.objects.filter(
            tournament_id=tournament_id, user_id=user_id).\
            values_list('round_match__round_no', flat=True))
        return max(round_nos)

    @classmethod
    def get_opponent_user_profile(cls, user_id, tournament_id, round_no):
        match_users = cls.objects.filter(
            round_match__round_no=round_no, tournament_id=tournament_id)

        opponent_user_id = cls._get_opponent_user_id(match_users, user_id)

        from .user import User
        user_profile = User.get_user_profile(opponent_user_id)
        return user_profile

    @classmethod
    def _get_opponent_user_id(cls, match_users, user_id):
        opponent_user_id = None
        for match_user in match_users:
            if user_id != match_user.user_id:
                opponent_user_id = match_user.user_id

        cls._validate_opponent_user_id(opponent_user_id)
        return opponent_user_id

    @classmethod
    def is_user_match_not_completed(cls, user_match):
        return not user_match.is_user_already_played()

    @classmethod
    def _validate_opponent_user_id(cls, user_id):
        from .user import User
        if User.is_user_id_null(user_id):
            raise Exception("Opponent is not set for given round")

    @classmethod
    def _validate_user_match(cls, match_id, user_id):
        if cls._is_user_match_not_available(match_id, user_id):
            raise Exception("Given user is not in the given match")

    @classmethod
    def _is_user_match_not_available(cls, match_id, user_id):
        return not cls._is_user_match_available(match_id, user_id)

    @classmethod
    def _is_user_match_available(cls, match_id, user_id):
        try:
            cls.get_match(match_id, user_id)
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_tournament_by_match_id(cls, match_id):
        match = cls.objects.get(round_match_id=match_id)
        return match.tournament

    def validate_play_match(self):
        if self.tournament.is_tournament_not_started():
            raise Exception("User can not play match until match is started")

        if self.is_user_already_played():
            raise Exception("user already played the match")

    @classmethod
    def user_submit_match_score(cls, user_match_score):
        from tdd_practice.constants.general import UserMatchStatus

        score = user_match_score['score']
        match_id = user_match_score['match_id']
        user_id = user_match_score['user_id']

        match = cls.get_match(round_match_id=match_id, user_id=user_id)
        match.update_score(score=score)
        match.update_status(status=UserMatchStatus.COMPLETED.value)

    @classmethod
    def get_match(cls, round_match_id, user_id):
        return cls.objects.get(round_match_id=round_match_id, user_id=user_id)

    def update_status(self, status):
        self.status = status
        self.save()

    def update_score(self, score):
        self.score = score
        self.save()

    @classmethod
    def create_user_matches(cls, match_id_wise_user_ids, tournament_id):
        for match_id, user_ids in match_id_wise_user_ids.items():
            for user_id in user_ids:
                Match.objects.create(user_id=user_id,
                                     round_match_id=match_id,
                                     tournament_id=tournament_id)

    def is_user_already_played(self):
        from tdd_practice.constants.general import UserMatchStatus
        return self.status == UserMatchStatus.COMPLETED.value
