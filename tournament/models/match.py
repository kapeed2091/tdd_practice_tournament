import random
from django.db import models
from django_swagger_utils.drf_server.exceptions import Forbidden, NotFound, BadRequest

from tournament.constants.exception_messages import MATCH_CAN_BE_PLAYED_ONLY_AFTER_THE_TOURNAMENT_HAS_STARTED, \
    USER_DOES_NOT_EXIST_WITH_THE_GIVEN_USER_ID, USER_DOES_NOT_BELONG_TO_THE_MATCH, \
    MATCH_DOES_NOT_EXIST_WITH_THE_GIVEN_MATCH_ID, THERE_ARE_NO_FURTHER_ROUNDS_IN_THIS_TOURNAMENT, \
    THERE_ARE_NO_VACANT_MATCHES, OPPONENT_IS_NOT_YET_ASSIGNED
from tournament.constants.general import MatchStatus, MatchUserStatus
from tournament.models import User, KoTournament


class Match(models.Model):
    MATCH_ID_LENGTH = 20
    STATUS_LENGTH = 20
    USER_STATUS_LENGTH = 20

    match_id = models.CharField(max_length=MATCH_ID_LENGTH)
    user = models.ForeignKey(User, blank=True, null=True)
    tournament = models.ForeignKey(KoTournament)
    score = models.IntegerField(default=0)
    round = models.IntegerField(default=0)
    status = models.CharField(max_length=STATUS_LENGTH)
    user_status = models.CharField(max_length=USER_STATUS_LENGTH, default=MatchUserStatus.NOT_DECIDED_YET.value)

    @classmethod
    def progress_match_winner_to_next_round(cls, match_id):
        winner_match = cls._get_winner_match(match_id)
        current_round = winner_match.round
        tournament = winner_match.tournament

        cls._validate_round_to_progress(
            tournament=tournament, current_round=current_round)
        match = cls.get_match_to_assign(
            match_round=current_round + 1,
            tournament=winner_match.tournament
        )
        match.assign_user_to_match(user=winner_match.user)

    @classmethod
    def get_match_to_assign(cls, match_round, tournament):
        matches = cls.objects.filter(
            round=match_round,
            tournament=tournament,
            user__isnull=True
        )

        if len(matches) == 0:
            raise NotFound(THERE_ARE_NO_VACANT_MATCHES)

        return random.choice(matches)

    def assign_user_to_match(self, user):
        self.user = user
        self.save()

    @classmethod
    def submit_score(cls, user_id, match_id, score):
        user = cls._get_user(user_id)
        cls._validate_match(match_id)
        match = cls._get_match(user=user, match_id=match_id)
        match.update_score(score=score)

    @classmethod
    def play_match(cls, user_id, match_id):
        user = cls._get_user(user_id)
        cls._validate_match(match_id)
        match = cls._get_match(user=user, match_id=match_id)
        cls._validate_tournament(tournament=match.tournament)
        match.update_status(status=MatchStatus.IN_PROGRESS.value)

    def update_status(self, status):
        self.status = status
        self.save()

    def update_score(self, score):
        self.score = score
        self.save()

    @classmethod
    def get_user_current_match(cls, user_id, tournament):
        user = cls._get_user(user_id)
        return cls.objects.filter(user=user, tournament=tournament).order_by('-round').first()

    @classmethod
    def get_opponent_user_of_match(cls, user, match_id):
        opponent_match = cls.objects.filter(
            match_id=match_id
        ).exclude(user=user).first()

        opponent_user = opponent_match.user
        cls._validate_opponent_user(opponent_user)
        return opponent_user

    @classmethod
    def get_tournament_winner_match(cls, tournament):
        final_round = tournament.no_of_rounds
        try:
            return cls.objects.get(
                round=final_round,
                tournament=tournament,
                user_status=MatchUserStatus.WIN.value
            )
        except cls.DoesNotExist:
            raise NotFound('Winner is not declared yet')

    @classmethod
    def get_user_match_in_a_tournament_round(cls, user, tournament_round, tournament):
        try:
            return cls.objects.get(
                user=user,
                round=tournament_round,
                tournament=tournament
            )
        except cls.DoesNotExist:
            raise NotFound('User has no match in the given round')

    @staticmethod
    def _validate_round_to_progress(tournament, current_round):
        if tournament.is_final_round(round_number=current_round):
            raise BadRequest(THERE_ARE_NO_FURTHER_ROUNDS_IN_THIS_TOURNAMENT)

    @classmethod
    def _get_winner_match(cls, match_id):
        return cls.objects.get(
            match_id=match_id,
            user_status=MatchUserStatus.WIN.value
        )

    @staticmethod
    def _get_user(user_id):
        from tournament.models import User

        try:
            return User.get_user(user_id)
        except User.DoesNotExist:
            raise NotFound(USER_DOES_NOT_EXIST_WITH_THE_GIVEN_USER_ID)

    @staticmethod
    def _validate_tournament(tournament):
        if tournament.is_not_started():
            raise Forbidden(MATCH_CAN_BE_PLAYED_ONLY_AFTER_THE_TOURNAMENT_HAS_STARTED)

    @classmethod
    def _get_match(cls, user, match_id):
        try:
            return cls.objects.get(user=user, match_id=match_id)
        except cls.DoesNotExist:
            raise Forbidden(USER_DOES_NOT_BELONG_TO_THE_MATCH)

    @classmethod
    def _validate_match(cls, match_id):
        if cls._does_not_match_exists(match_id):
            raise NotFound(MATCH_DOES_NOT_EXIST_WITH_THE_GIVEN_MATCH_ID)

    @classmethod
    def _does_not_match_exists(cls, match_id):
        return not cls._does_match_exists(match_id)

    @classmethod
    def _does_match_exists(cls, match_id):
        return cls.objects.filter(match_id=match_id).exists()

    @staticmethod
    def _validate_opponent_user(opponent_user):
        if opponent_user is None:
            raise NotFound(OPPONENT_IS_NOT_YET_ASSIGNED)

