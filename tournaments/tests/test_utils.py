from django.test import TestCase
from tournaments.constants.general import TournamentStatus, \
    UserTournamentStatus
from tournaments.constants.general import DEFAULT_SCORE


class TestUtils(TestCase):
    @staticmethod
    def create_tournament(
            user_id, status=TournamentStatus.IN_PROGRESS.value):
        from tournaments.models import Tournament

        total_rounds = 4

        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        start_datetime = get_current_local_date_time()

        tournament = Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime,
            status=status
        )

        return tournament

    @staticmethod
    def create_user(name="John"):
        from tournaments.models import User

        user = User.objects.create(name=name)
        return user

    @staticmethod
    def create_match(tournament_id, round_number):
        from tournaments.models import Match

        match = Match.objects.create(
            tournament_id=tournament_id,
            round_number=round_number
        )

        return match

    @staticmethod
    def create_user_tournament(
            user_id, tournament_id, status=UserTournamentStatus.ALIVE.value,
            round_number=1
    ):
        from tournaments.models import UserTournament

        obj = UserTournament.objects.create(
            user_id=user_id,
            tournament_id=tournament_id,
            status=status,
            round_number=round_number
        )
        return obj

    @staticmethod
    def create_user_match(user_id, match_id, score=DEFAULT_SCORE):
        from tournaments.models import UserMatch

        obj = UserMatch.objects.create(
            user_id=user_id,
            match_id=match_id,
            score=score
        )

        return obj

    @staticmethod
    def create_tournament_matches(tournament_id, total_rounds):
        from tournaments.models import Match

        for each_round in range(total_rounds, 0, -1):
            matches_to_be_created = 2 ** (total_rounds - each_round)
            for each in range(matches_to_be_created):
                Match.objects.create(
                    tournament_id=tournament_id,
                    round_number=each_round
                )

    @staticmethod
    def create_tournament_matches_(tournament_id, total_rounds):
        from tournaments.models import Match

        matches = []
        for each_round in range(total_rounds, 0, -1):
            matches_to_be_created = 2 ** (total_rounds - each_round)
            for each in range(matches_to_be_created):
                obj = Match.objects.create(
                    tournament_id=tournament_id,
                    round_number=each_round
                )
                matches.append(obj)

        return matches

    @staticmethod
    def assign_players_to_matches(matches, players):
        from tournaments.models import UserMatch
        total_players = len(players)

        for index, match in enumerate(matches):
            print (index, players, "LKI"*10)
            player = players[index]
            user_id_1 = player.user_id
            UserMatch.objects.create(
                user_id=user_id_1,
                match_id=match.id,
                score=DEFAULT_SCORE
            )

            opponent_player = players[total_players - 1 - index]
            user_id_2 = opponent_player.user_id
            UserMatch.objects.create(
                user_id=user_id_2,
                match_id=match.id,
                score=DEFAULT_SCORE
            )
