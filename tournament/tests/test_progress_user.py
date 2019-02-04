from django.test import TestCase
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

import datetime

from tournament.constants.general import TournamentStatus, MatchUserStatus, MatchStatus


class TestProgressUser(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    user2_id = 'User2'
    match1_id = 'Match1'
    match2_id = 'Match2'

    def setUp(self):
        from tournament.models import User, KoTournament, Match

        now = get_current_datetime()
        user1 = User.objects.create(
            user_id=self.user1_id
        )
        user2 = User.objects.create(
            user_id=self.user2_id
        )
        tournament = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament',
            no_of_rounds=2,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user1,
            tournament=tournament,
            score=20,
            round=1,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.WIN.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user2,
            tournament=tournament,
            score=10,
            round=1,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.LOST.value
        )
        Match.objects.create(
            match_id=self.match2_id,
            tournament=tournament,
            round=2,
            status=MatchStatus.YET_TO_START.value,
        )

    def test_progress_winner_to_next_round(self):
        from tournament.models import Match, User

        match2_before = Match.objects.get(match_id=self.match2_id)
        self.assertEqual(match2_before.user, None)
        Match.progress_match_winner_to_next_round(match_id=self.match1_id)

        user1 = User.objects.get(user_id=self.user1_id)
        match2_after = Match.objects.get(match_id=self.match2_id)
        self.assertEqual(match2_after.user, user1)
