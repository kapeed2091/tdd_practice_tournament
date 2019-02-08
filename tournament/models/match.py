import random
from django.db import models
from django_swagger_utils.drf_server.exceptions import Forbidden, NotFound, BadRequest

from tournament.constants.exception_messages import MATCH_CAN_BE_PLAYED_ONLY_AFTER_THE_TOURNAMENT_HAS_STARTED, \
    USER_DOES_NOT_BELONG_TO_THE_MATCH, MATCH_DOES_NOT_EXIST_WITH_THE_GIVEN_MATCH_ID, \
    THERE_ARE_NO_FURTHER_ROUNDS_IN_THIS_TOURNAMENT, THERE_ARE_NO_VACANT_MATCHES, \
    OPPONENT_IS_NOT_YET_ASSIGNED, USER_HAS_NO_MATCH_IN_THE_GIVEN_ROUND, WINNER_IS_NOT_DECLARED_YET, INVALID_USER_ID
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
        next_round = cls._get_next_round_to_progress(winner_match)
        match = cls.get_match_to_assign(
            match_round=next_round,
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
        match = cls._get_user_match(user_id=user_id, match_id=match_id)
        match.update_score(score=score)

    @classmethod
    def play_match(cls, user_id, match_id):
        match = cls._get_user_match(user_id=user_id, match_id=match_id)
        cls._validate_user_match_to_play(match)
        match.update_status(status=MatchStatus.IN_PROGRESS.value)

    def update_status(self, status):
        self.status = status
        self.save()

    def update_score(self, score):
        self.score = score
        self.save()

    @classmethod
    def get_user_current_match(cls, user_id, tournament):
        from tournament.models import User

        user = User.get_user(user_id)
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
            raise NotFound(WINNER_IS_NOT_DECLARED_YET)

    @classmethod
    def get_user_match_in_a_tournament(cls, user, tournament_round, tournament_id):
        from tournament.models import KoTournament, TournamentUser

        tournament = KoTournament.get_tournament(tournament_id)
        tournament.validate_tournament_round(tournament_round)
        TournamentUser.validate_tournament_user(user=user, tournament=tournament)
        try:
            return cls.objects.get(
                user=user,
                round=tournament_round,
                tournament=tournament
            )
        except cls.DoesNotExist:
            raise NotFound(USER_HAS_NO_MATCH_IN_THE_GIVEN_ROUND)

    @classmethod
    def _get_next_round_to_progress(cls, user_match):
        cls._validate_weather_there_is_next_round(user_match)
        return user_match.round + 1

    @staticmethod
    def _validate_weather_there_is_next_round(user_match):
        # TODO: Refactor method name
        tournament = user_match.tournament
        if tournament.is_final_round(round_number=user_match.round):
            raise BadRequest(THERE_ARE_NO_FURTHER_ROUNDS_IN_THIS_TOURNAMENT)

    @classmethod
    def _get_winner_match(cls, match_id):
        return cls.objects.get(
            match_id=match_id,
            user_status=MatchUserStatus.WIN.value
        )

    @classmethod
    def _get_user_match(cls, user_id, match_id):
        # TODO: Refactor
        from tournament.models import User

        user = User.get_user(user_id)
        cls._validate_match(match_id)
        try:
            return cls.objects.get(user=user, match_id=match_id)
        except cls.DoesNotExist:
            raise Forbidden(USER_DOES_NOT_BELONG_TO_THE_MATCH)

    @classmethod
    def _validate_user_match_to_play(cls, match):
        tournament = match.tournament
        if tournament.is_not_started():
            raise Forbidden(MATCH_CAN_BE_PLAYED_ONLY_AFTER_THE_TOURNAMENT_HAS_STARTED)


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

