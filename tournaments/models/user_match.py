from django.db import models
from tournaments.constants.general import DEFAULT_SCORE


class UserMatch(models.Model):
    user_id = models.PositiveIntegerField()
    match_id = models.PositiveIntegerField()
    score = models.IntegerField(default=DEFAULT_SCORE)

    # todo: feedback too much information
    # todo: renaming function - play match
    @classmethod
    def create_user_match(cls, user_id, match_id):
        # todo feedback obscured intent
        # todo feedback: G30 functions should do one thing
        from .user import User
        User.validate_user_id(user_id=user_id)

        from .match import Match
        match = Match.validate_and_get_match_by_id(match_id=match_id)

        from .user_tournament import UserTournament
        tournament_id = match.tournament_id
        UserTournament.validate_user_in_tournament(
            user_id=user_id, tournament_id=tournament_id
        )

        from tournaments.constants.general import UserTournamentStatus
        from .user_tournament import UserTournament
        # todo: feedback artificial coupling, feature envy,
        #  misplaced responsibility
        # todo: feedback make logical dependencies physical --> assumed user
        #  no longer available tournament when status is DEAD
        # todo: feedback encapsulating boundary condition
        # todo: feedback one level of abstraction
        is_user_dead = UserTournament.objects.filter(
            user_id=user_id, tournament_id=tournament_id,
            status=UserTournamentStatus.DEAD.value
        ).exists()

        if is_user_dead:
            from tournaments.exceptions.custom_exceptions import \
                UserNotInTournamentAnymore
            raise UserNotInTournamentAnymore

        cls._validate_match_users_count(match_id=match.id)

        round_number = match.round_number
        from .tournament import Tournament
        players_count = Tournament.get_players_count_in_a_round(
            tournament_id=tournament_id, round_number=round_number
        )

        from .user_tournament import UserTournament
        # todo: feedback inconsistency
        current_players_count = \
            UserTournament.get_current_players_count_in_round(
                tournament_id=tournament_id, round_number=round_number
            )

        # todo: feedback encapsulating boundary condition
        # todo: feedback encapsulating conditionals
        if current_players_count < players_count:
            from tournaments.exceptions.custom_exceptions import \
                InsufficientMembersInRoundToPlayMatch
            raise InsufficientMembersInRoundToPlayMatch

        cls.objects.create(
            user_id=user_id,
            match_id=match_id
        )

    def submit_score(self, score):
        self.validate_score(score=score)

        self._update_score(score=score)

    # todo feedback artificial coupling ???
    @classmethod
    def assign_players(cls, tournament_id, round_number):
        # todo: feedback inconsistency in (tournament object only for rounds)
        # todo feedback: G30 functions should do one thing
        from .tournament import Tournament
        tournament = Tournament.get_tournament_by_id(
            tournament_id=tournament_id
        )

        # todo feedback: misplaced responsibility, artificial coupling
        cls.validate_round_number(
            total_rounds=tournament.total_rounds, round_number=round_number
        )

        players_count_in_a_round = Tournament.get_players_count_in_a_round(
            tournament_id=tournament_id, round_number=round_number
        )

        from .user_tournament import UserTournament

        # ToDo FEEDBACK Code at Wrong Level of Abstraction
        players = UserTournament.get_players_that_reached_round_alive(
            tournament_id=tournament_id, round_number=round_number
        )
        total_players = len(players)

        # todo feedback: misplaced responsibility, artificial coupling
        cls.validate_players_count_in_round(
            total_players=total_players,
            players_count_in_a_round=players_count_in_a_round
        )

        from .match import Match
        matches = Match.get_matches_by_tournament_and_round(
            tournament_id=tournament_id, round_number=round_number
        )
        total_matches = len(matches)

        cls.validate_number_of_matches(
            total_matches=total_matches, total_players=total_players
        )

        match_ids = [each.id for each in matches]
        cls.validate_user_matches(match_ids=match_ids)

        # todo: feedback function should descend only one level of abstraction
        for index, match in enumerate(matches):
            # todo: feedback inconsistency in naming of players and user_ids
            # todo feedback coupling of match making and object creation
            player = players[index]
            user_id_1 = player.user_id
            cls.objects.create(
                user_id=user_id_1,
                match_id=match.id,
                score=DEFAULT_SCORE
            )

            opponent_player = players[total_players - 1 - index]
            user_id_2 = opponent_player.user_id
            cls.objects.create(
                user_id=user_id_2,
                match_id=match.id,
                score=DEFAULT_SCORE
            )

    @classmethod
    def get_opponent_player_details(cls, user_id, tournament_id):
        from .user_tournament import UserTournament

        user_tournament = UserTournament.validate_and_get_user_tournament(
            user_id=user_id, tournament_id=tournament_id
        )

        user_tournament.validate_if_user_is_alive()

        from .match import Match

        round_number = user_tournament.round_number
        # todo feedback: bug - multiple
        match = Match.objects.get(
            tournament_id=tournament_id, round_number=round_number
        )

        opponents = cls._validate_if_opponent_is_assigned_and_get_opponents(
            user_id=user_id, match_id=match.id
        )

        # todo: feedback function should descend only one level of abstraction
        opponent = opponents[0]
        opponent_user_id = opponent.user_id

        # todo feedback feature envy
        from .user import User
        user_obj = User.get_user_by_id(user_id=opponent_user_id)
        user_details = user_obj.convert_to_dict()

        return user_details

    @classmethod
    def get_user_matches(cls, match_id):
        objs = cls.objects.filter(match_id=match_id)
        return objs

    def validate_score(self, score):
        if score < 0:
            from tournaments.exceptions.custom_exceptions import InvalidScore
            raise InvalidScore

        # todo feedback: misplaced responsibility

        # todo: feedback encapsulating boundary condition
        # todo: feedback encapsulating conditionals to make it more readable
        if self.score != DEFAULT_SCORE:
            from tournaments.exceptions.custom_exceptions import \
                ScoreCannotBeUpdated
            raise ScoreCannotBeUpdated

    # todo feedback artificial coupling
    @staticmethod
    def validate_players_count_in_round(total_players,
                                        players_count_in_a_round):
        if total_players != players_count_in_a_round:
            from tournaments.exceptions.custom_exceptions import \
                InsufficientMembersInRound
            raise InsufficientMembersInRound

    # todo feedback artificial coupling
    @staticmethod
    def validate_number_of_matches(total_matches, total_players):
        from tournaments.constants.general import MAX_NUM_OF_PEOPLE_FOR_MATCH

        # todo: feedback encapsulating conditionals
        if total_matches * MAX_NUM_OF_PEOPLE_FOR_MATCH != total_players:
            from tournaments.exceptions.custom_exceptions import \
                InadequateNumberOfMatches
            raise InadequateNumberOfMatches

    @classmethod
    def validate_user_matches(cls, match_ids):
        user_matches_exist = cls.objects.filter(
            match_id__in=match_ids
        ).exists()

        if user_matches_exist:
            from tournaments.exceptions.custom_exceptions import \
                ReAssignmentOfPlayers
            raise ReAssignmentOfPlayers

    # todo: feedback misplaced responsibility
    @staticmethod
    def validate_round_number(total_rounds, round_number):
        if total_rounds < round_number:
            from tournaments.exceptions.custom_exceptions import \
                RoundNumberOutOfBounds
            raise RoundNumberOutOfBounds

    # todo feedback be precise
    @classmethod
    def validate_if_match_in_progress(cls, match_id):
        # todo: feedback duplicate
        user_matches = cls.objects.filter(match_id=match_id)

        for each_user_match in user_matches:
            # todo: feedback DEFAULT_SCORE is doing two things: maintaining
            #  score and state of Match
            if each_user_match.score == DEFAULT_SCORE:
                from tournaments.exceptions.custom_exceptions import \
                    MatchInProgress
                raise MatchInProgress

    # todo: feedback vertical separation
    def _update_score(self, score):
        self.score = score
        self.save()

    @classmethod
    def _validate_match_users_count(cls, match_id):
        match_id_users_count = cls.objects.filter(match_id=match_id).count()

        from tournaments.constants.general import MAX_NUM_OF_PEOPLE_FOR_MATCH
        if match_id_users_count >= MAX_NUM_OF_PEOPLE_FOR_MATCH:
            from tournaments.exceptions.custom_exceptions import \
                MatchIdOverused
            raise MatchIdOverused

    # todo feedback be precise
    @classmethod
    def _validate_if_opponent_is_assigned_and_get_opponents(
            cls, match_id, user_id
    ):
        # todo: feedback function should only one thing
        opponents = cls.objects.filter(match_id=match_id).exclude(
            user_id=user_id)
        # todo: negative conditionals
        if not opponents:
            from tournaments.exceptions.custom_exceptions import \
                OpponentNotYetAssigned
            raise OpponentNotYetAssigned

        return opponents
