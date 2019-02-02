from django.test import TestCase
from tournaments.constants.general import TournamentStatus


class TestSubmitScore(TestCase):
    def test_submit_score(self):
        from tournaments.models import UserMatch

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )
        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        user_match = self.create_user_match(
            user_id=user.id, match_id=match.id
        )

        score = 200
        user_match.submit_score(score=score)

        user_match_obj = UserMatch.objects.get(
            user_id=user.id, match_id=match.id
        )
        self.assertEqual(user_match_obj.score, score)

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
    def create_user_match(user_id, match_id):
        from tournaments.models import UserMatch
        from tournaments.constants.general import DEFAULT_SCORE

        obj = UserMatch.objects.create(
            user_id=user_id,
            match_id=match_id,
            score=DEFAULT_SCORE
        )

        return obj
