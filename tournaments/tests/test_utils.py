from django.test import TestCase
from tournaments.constants.general import TournamentStatus
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
    def create_user_tournament(user_id, tournament_id):
        from tournaments.models import UserTournament

        obj = UserTournament.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
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
