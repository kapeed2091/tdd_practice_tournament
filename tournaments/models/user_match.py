from django.db import models
from tournaments.constants.general import DEFAULT_SCORE


class UserMatch(models.Model):
    user_id = models.PositiveIntegerField()
    match_id = models.PositiveIntegerField()
    score = models.IntegerField(default=DEFAULT_SCORE)

    @classmethod
    def create_user_match(cls, user_id, match_id):
        from .user import User
        User.validate_user_id(user_id=user_id)

        from .match import Match
        match = Match.validate_and_get_match_by_id(match_id=match_id)

        tournament_id = match.tournament_id

        from .user_tournament import UserTournament
        UserTournament.validate_user_in_tournament(
            user_id=user_id, tournament_id=tournament_id
        )

        match_id_users_count = cls.objects.filter(match_id=match_id).count()

        if match_id_users_count >= 2:
            from tournaments.exceptions.custom_exceptions import \
                MatchIdOverused
            raise MatchIdOverused

        cls.objects.create(
            user_id=user_id,
            match_id=match_id
        )

    def submit_score(self, score):
        self.validate_score(score=score)

        self._update_score(score=score)

    def _update_score(self, score):
        self.score = score
        self.save()

    def validate_score(self, score):
        if score < 0:
            from tournaments.exceptions.custom_exceptions import InvalidScore
            raise InvalidScore

        if self.score != DEFAULT_SCORE:
            from tournaments.exceptions.custom_exceptions import \
                ScoreCannotBeUpdated
            raise ScoreCannotBeUpdated
