from django.db import models


class UserTournament(models.Model):
    STATUS_MAX_LENGTH = 20

    user_id = models.PositiveIntegerField()
    tournament_id = models.PositiveIntegerField()
    status = models.CharField(max_length=STATUS_MAX_LENGTH)
    round_number = models.IntegerField()

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from ..models import User, Tournament

        User.validate_user_id(user_id=user_id)

        Tournament.validate_tournament_id(tournament_id=tournament_id)

        cls._validate_user_tournament_exists(
            user_id=user_id, tournament_id=tournament_id
        )

        tournament = Tournament.get_tournament_by_id(
            tournament_id=tournament_id
        )

        Tournament.validate_tournament_status(status=tournament.status)

        is_last_person = cls._is_last_person(
            tournament_id=tournament_id, total_rounds=tournament.total_rounds
        )

        from tournaments.constants.general import UserTournamentStatus, \
            DEFAULT_USER_TOURNAMENT_ROUND_NUMBER
        cls.objects.create(
            user_id=user_id,
            tournament_id=tournament_id,
            status=UserTournamentStatus.ALIVE.value,
            round_number=DEFAULT_USER_TOURNAMENT_ROUND_NUMBER
        )

        if is_last_person:
            from ..constants.general import TournamentStatus
            tournament.update_status(
                status=TournamentStatus.FULL_YET_TO_START.value
            )

    @classmethod
    def level_up(cls, user_id, match_id):
        from .match import Match
        match = Match.validate_and_get_match_by_id(match_id=match_id)

        tournament_id = match.tournament_id
        user_tournament = cls.objects.get(
            user_id=user_id, tournament_id=tournament_id
        )

        cls._validate_if_level_up_is_done_already(
            user_tournament=user_tournament, match=match
        )

        cls._validate_if_user_in_match(user_id=user_id, match_id=match_id)

        cls._validate_if_user_is_winner(user_id=user_id, match_id=match_id)

        user_tournament.update_round_number(
            round_number=match.round_number + 1
        )

    @classmethod
    def can_user_play_in_tournament(cls, user_id, tournament_id):
        from ..exceptions.custom_exceptions import UserNotInTournament

        user_in_tournament = cls.objects.filter(
            user_id=user_id, tournament_id=tournament_id
        ).exists()

        if not user_in_tournament:
            raise UserNotInTournament

        from ..models.tournament import Tournament
        tournament = Tournament.get_tournament_by_id(
            tournament_id=tournament_id
        )

        from ..constants.general import TournamentStatus
        if tournament.status == TournamentStatus.IN_PROGRESS.value:
            return True
        return False

    def update_round_number(self, round_number):
        self.round_number = round_number
        self.save()

    @classmethod
    def _validate_user_tournament_exists(cls, user_id, tournament_id):
        user_tournament_exists = cls.objects.filter(
            user_id=user_id, tournament_id=tournament_id
        )

        if user_tournament_exists:
            from ..exceptions.custom_exceptions import UserAlreadyRegistered
            raise UserAlreadyRegistered

    @classmethod
    def _is_last_person(cls, tournament_id, total_rounds):
        total_rounds = total_rounds
        max_num_of_participants = 2 ** total_rounds
        registered_tournament_members_count = \
            cls.objects.filter(tournament_id=tournament_id).count()

        is_last_person = \
            max_num_of_participants - 1 == registered_tournament_members_count

        return is_last_person

    @classmethod
    def validate_user_in_tournament(cls, user_id, tournament_id):
        user_in_tournament = UserTournament.objects.filter(
            user_id=user_id,
            tournament_id=tournament_id
        ).exists()

        if not user_in_tournament:
            from tournaments.exceptions.custom_exceptions import \
                UserNotInTournament
            raise UserNotInTournament

    @classmethod
    def _validate_if_level_up_is_done_already(cls, user_tournament, match):
        if match.round_number <= user_tournament.round_number - 1:
            from tournaments.exceptions.custom_exceptions import \
                UserAlreadyLeveledUp
            raise UserAlreadyLeveledUp

    @staticmethod
    def _validate_if_user_in_match(user_id, match_id):
        from .user_match import UserMatch
        user_match_exists = UserMatch.objects.filter(
            user_id=user_id, match_id=match_id
        ).exists()

        if not user_match_exists:
            from tournaments.exceptions.custom_exceptions import UserNotInMatch
            raise UserNotInMatch

    @staticmethod
    def _validate_if_user_is_winner(user_id, match_id):
        from .user_match import UserMatch
        user_matches = UserMatch.objects.filter(match_id=match_id)
        user_matches = sorted(user_matches, key=lambda x: x.score,
                              reverse=True)
        user_match_with_max_score = user_matches[0]

        if user_match_with_max_score.user_id != user_id:
            from tournaments.exceptions.custom_exceptions import \
                UserDidNotWinMatch
            raise UserDidNotWinMatch
