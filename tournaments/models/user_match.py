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

        from tournaments.constants.general import UserTournamentStatus
        from .user_tournament import UserTournament
        is_user_dead = UserTournament.objects.filter(
            user_id=user_id, tournament_id=tournament_id,
            status=UserTournamentStatus.DEAD.value
        ).exists()

        if is_user_dead:
            from tournaments.exceptions.custom_exceptions import \
                UserNotInTournamentAnymore
            raise UserNotInTournamentAnymore

        cls._validate_match_users_count(match_id=match.id)

        cls.objects.create(
            user_id=user_id,
            match_id=match_id
        )

    def submit_score(self, score):
        self.validate_score(score=score)

        self._update_score(score=score)

    @classmethod
    def assign_players(cls, tournament_id, round_number):
        from .user_tournament import UserTournament
        players = UserTournament.get_players_that_reached_round_alive(
            tournament_id=tournament_id, round_number=round_number
        )
        total_players = len(players)

        from .tournament import Tournament
        tournament = Tournament.get_tournament_by_id(
            tournament_id=tournament_id
        )
        total_rounds = tournament.total_rounds
        total_players_that_should_play_in_round = 2 ** (
                total_rounds + 1 - round_number)

        if total_players != total_players_that_should_play_in_round:
            from tournaments.exceptions.custom_exceptions import \
                InsufficientMembersInRound
            raise InsufficientMembersInRound

        from .match import Match
        matches = Match.get_matches_by_tournament_and_round(
            tournament_id=tournament_id, round_number=round_number
        )

        for index, match in enumerate(matches):
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

    @classmethod
    def _validate_match_users_count(cls, match_id):
        match_id_users_count = cls.objects.filter(match_id=match_id).count()

        from tournaments.constants.general import MAX_NUM_OF_PEOPLE_FOR_MATCH
        if match_id_users_count >= MAX_NUM_OF_PEOPLE_FOR_MATCH:
            from tournaments.exceptions.custom_exceptions import \
                MatchIdOverused
            raise MatchIdOverused
