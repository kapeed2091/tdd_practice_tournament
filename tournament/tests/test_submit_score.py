from django.test import TestCase
from django_swagger_utils.drf_server.exceptions import NotFound
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

import datetime

from tournament.constants.general import TournamentStatus, MatchStatus


class TestSubmitScore(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    invalid_user_id = 'InvalidUser'
    match_id = 'Match'

    def setUp(self):
        from tournament.models import User, KoTournament, Match

        now = get_current_datetime()
        user = User.objects.create(
            user_id=self.user1_id
        )
        tournament = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament',
            no_of_rounds=2,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )
        Match.objects.create(
            match_id=self.match_id,
            user=user,
            tournament=tournament,
            status=MatchStatus.IN_PROGRESS.value
        )

    def test_submit_score(self):
        from tournament.models import User, Match

        user = User.get_user(user_id=self.user1_id)
        match_before = Match.objects.get(user=user, match_id=self.match_id)
        self.assertEqual(match_before.score, 0)
        Match.submit_score(
            user_id=self.user1_id,
            match_id=self.match_id,
            score=10)
        match_after = Match.objects.get(user=user, match_id=self.match_id)
        self.assertEqual(match_after.score, 10)

    def test_submit_score_with_invalid_user(self):
        from tournament.models import Match

        with self.assertRaisesMessage(NotFound, 'User does not exist with the given user id'):
            Match.submit_score(
                user_id=self.invalid_user_id,
                match_id=self.match_id,
                score=10
            )
