from django.db import models


class UserTournament(models.Model):
    STATUS_MAX_LENGTH = 20

    user_id = models.PositiveIntegerField()
    tournament_id = models.PositiveIntegerField()
    status = models.CharField(max_length=STATUS_MAX_LENGTH)
    round_number = models.IntegerField()

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        # todo: feedback too much information
        # todo feedback: G30 functions should do one thing
        from ..models import User, Tournament

        User.validate_user_id(user_id=user_id)

        Tournament.validate_tournament_id(tournament_id=tournament_id)

        # todo feedback: inconsistency in naming
        cls._validate_user_tournament_exists(
            user_id=user_id, tournament_id=tournament_id
        )

        tournament = Tournament.get_tournament_by_id(
            tournament_id=tournament_id
        )
        tournament.validate_tournament_status()

        is_last_person = cls._is_last_person(
            tournament_id=tournament_id, total_rounds=tournament.total_rounds
        )
        if is_last_person:
            from ..constants.general import TournamentStatus
            tournament.update_status(
                status=TournamentStatus.FULL_YET_TO_START.value
            )

        from tournaments.constants.general import UserTournamentStatus, \
            DEFAULT_USER_TOURNAMENT_ROUND_NUMBER
        cls.objects.create(
            user_id=user_id,
            tournament_id=tournament_id,
            status=UserTournamentStatus.ALIVE.value,
            round_number=DEFAULT_USER_TOURNAMENT_ROUND_NUMBER
        )

    @classmethod
    def level_up(cls, user_id, match_id):
        # todo feedback: G30 functions should do one thing
        from .user import User
        User.validate_user_id(user_id=user_id)

        from .match import Match
        match = Match.validate_and_get_match_by_id(match_id=match_id)

        tournament_id = match.tournament_id
        # ToDo FEEDBACK Duplication
        user_tournament = cls.objects.get(
            user_id=user_id, tournament_id=tournament_id
        )

        from .user_match import UserMatch
        UserMatch.validate_if_match_in_progress(match_id=match_id)

        cls._validate_if_level_up_is_done_already(
            user_tournament=user_tournament, match=match
        )

        cls._validate_if_user_in_match(user_id=user_id, match_id=match_id)

        cls._validate_if_user_is_winner(user_id=user_id, match_id=match_id)

        from .tournament import Tournament
        tournament = Tournament.get_tournament_by_id(
            tournament_id=tournament_id
        )

        # todo feedback: encapsulating conditionals
        # todo: feedback function should descend only one level of abstraction
        if tournament.total_rounds == match.round_number:
            from tournaments.constants.general import TournamentStatus
            tournament.update_status(status=TournamentStatus.COMPLETED.value)
        else:
            user_tournament.update_round_number(
                round_number=match.round_number + 1
            )

    # todo feedback remove code
    @classmethod
    def can_user_play_in_tournament(cls, user_id, tournament_id):
        # todo: feedback functions should do only one thing
        from ..exceptions.custom_exceptions import UserNotInTournament
        # ToDo FEEDBACK Obvious Behavior Is Unimplemented
        user_in_tournament = cls.is_user_in_tournament(
            user_id=user_id, tournament_id=tournament_id
        )

        # todo: feedback negative conditionals
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

    @classmethod
    def update_loser_status(cls, match_id):
        from .match import Match
        match = Match.validate_and_get_match_by_id(match_id=match_id)

        # todo feedback: G30 functions should do one thing
        # todo feedback feature envy ???
        from .user_match import UserMatch
        user_matches = UserMatch.get_user_matches(match_id=match_id)

        # todo: feedback make logical dependencies physical
        user_matches_sorted = sorted(user_matches, key=lambda x: x.score)
        user_match_with_lowest_score = user_matches_sorted[0]

        user_id = user_match_with_lowest_score.user_id
        tournament_id = match.tournament_id

        user_tournament = cls.get_user_tournament_by_details(
            user_id=user_id,
            tournament_id=tournament_id
        )

        user_tournament.validate_if_user_status_has_been_updated()

        user_tournament.update_player_status_to_dead()

    def update_round_number(self, round_number):
        self.round_number = round_number
        self.save()

    def update_player_status_to_dead(self):
        from tournaments.constants.general import UserTournamentStatus

        self.status = UserTournamentStatus.DEAD.value
        self.save()

    # todo: feedback obvious behavior is unimplemented
    @classmethod
    def get_players_that_reached_round_alive(cls, tournament_id, round_number):
        from tournaments.constants.general import UserTournamentStatus

        players = cls.objects.filter(
            tournament_id=tournament_id,
            status=UserTournamentStatus.ALIVE.value,
            round_number=round_number
        )

        return players

    @classmethod
    def get_current_round_number(cls, user_id, tournament_id):
        # ToDo FEEDBACK Duplication
        try:
            obj = cls.objects.get(user_id=user_id, tournament_id=tournament_id)
            return obj.round_number
        except cls.DoesNotExist:
            from tournaments.exceptions.custom_exceptions import \
                UserNotInTournament
            raise UserNotInTournament

    # todo: feedback obvious behavior is unimplemented,
    #  we expect user object in return for this function,
    #  returning user_tournament object
    @classmethod
    def get_winner(cls, tournament_id):
        from .tournament import Tournament
        tournament = Tournament.get_tournament_by_id(
            tournament_id=tournament_id
        )

        tournament.validate_if_status_is_completed()

        from tournaments.constants.general import UserTournamentStatus

        total_rounds = tournament.total_rounds
        user_tournament = cls.objects.get(
            tournament_id=tournament_id, round_number=total_rounds,
            status=UserTournamentStatus.ALIVE.value
        )

        return user_tournament

    @classmethod
    def is_user_in_tournament(cls, user_id, tournament_id):
        user_tournament_exists = cls.objects.filter(
            user_id=user_id, tournament_id=tournament_id
        ).exists()

        return user_tournament_exists

    @classmethod
    def get_user_tournament_by_details(cls, user_id, tournament_id):
        obj = cls.objects.get(
            user_id=user_id, tournament_id=tournament_id
        )
        return obj

    # todo: feedback name should be changed ???
    @classmethod
    def get_current_players_count_in_round(cls, tournament_id, round_number):
        from tournaments.constants.general import UserTournamentStatus

        players_count = cls.objects.filter(
            tournament_id=tournament_id,
            round_number=round_number,
            status=UserTournamentStatus.ALIVE.value
        ).count()

        return players_count

    @classmethod
    def validate_user_in_tournament(cls, user_id, tournament_id):
        # ToDo FEEDBACK Duplication
        user_in_tournament = UserTournament.objects.filter(
            user_id=user_id,
            tournament_id=tournament_id
        ).exists()

        if not user_in_tournament:
            from tournaments.exceptions.custom_exceptions import \
                UserNotInTournament
            raise UserNotInTournament

    @classmethod
    def validate_and_get_user_tournament(cls, user_id, tournament_id):
        try:
            obj = cls.get_user_tournament_by_details(
                user_id=user_id, tournament_id=tournament_id
            )
            return obj
        except cls.DoesNotExist:
            from tournaments.exceptions.custom_exceptions import \
                UserNotInTournament
            raise UserNotInTournament

    # todo: feedback obvious behavior is unimplemented
    def validate_if_user_is_alive(self):
        from tournaments.constants.general import UserTournamentStatus

        if self.status == UserTournamentStatus.DEAD.value:
            from tournaments.exceptions.custom_exceptions import \
                UserNotInTournamentAnymore
            raise UserNotInTournamentAnymore

    # todo: feedback obvious behavior is unimplemented, obscured intent
    def validate_if_user_status_has_been_updated(self):
        from tournaments.constants.general import UserTournamentStatus

        if self.status == UserTournamentStatus.DEAD.value:
            from tournaments.exceptions.custom_exceptions import \
                LoserStatusAlreadyUpdated
            raise LoserStatusAlreadyUpdated

    # todo: feedback vertical separation
    @classmethod
    def _is_last_person(cls, tournament_id, total_rounds):
        total_rounds = total_rounds
        # todo: feedback make logical dependencies physical
        max_num_of_participants = 2 ** total_rounds
        registered_tournament_members_count = \
            cls.objects.filter(tournament_id=tournament_id).count()

        # todo not standard convention ???
        is_last_person = \
            max_num_of_participants - 1 == registered_tournament_members_count

        return is_last_person

    @classmethod
    def _validate_user_tournament_exists(cls, user_id, tournament_id):
        user_tournament_exists = cls.is_user_in_tournament(
            user_id=user_id, tournament_id=tournament_id
        )

        if user_tournament_exists:
            from ..exceptions.custom_exceptions import UserAlreadyRegistered
            raise UserAlreadyRegistered

    @classmethod
    def _validate_if_level_up_is_done_already(cls, user_tournament, match):
        # todo: feedback encapsulating conditionals
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

        # todo: feedback negative conditionals
        if not user_match_exists:
            from tournaments.exceptions.custom_exceptions import UserNotInMatch
            raise UserNotInMatch

    # todo: feedback function should only one thing
    @staticmethod
    def _validate_if_user_is_winner(user_id, match_id):
        from .user_match import UserMatch
        user_matches = UserMatch.objects.filter(match_id=match_id)
        # todo: feedback make logical dependencies physical
        user_matches = sorted(user_matches, key=lambda x: x.score,
                              reverse=True)
        user_match_with_max_score = user_matches[0]

        if user_match_with_max_score.user_id != user_id:
            from tournaments.exceptions.custom_exceptions import \
                UserDidNotWinMatch
            raise UserDidNotWinMatch
