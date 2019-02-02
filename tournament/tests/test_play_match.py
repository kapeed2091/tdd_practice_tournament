from django.test import TestCase
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

import datetime

from tournament.constants.general import TournamentStatus


class TestPlayMatch(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    match1_id = 'Match1'

    def setUp(self):
        from tournament.models import User, KoTournament, Match

        now = get_current_datetime()
        user1 = User.objects.create(
            user_id=self.user1_id
        )
        tournament1 = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament1',
            no_of_rounds=2,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )

        Match.objects.create(
            match_id=self.match1_id,
            user=user1,
            tournament=tournament1,
            status=MatchStatus.YET_TO_START.value
        )

    def test_user_will_play_match(self):
        from tournament.models import Match

        match_before = Match.objects.get(user_id=self.user1_id, match_id=self.match1_id)
        self.assertEqual(match_before.status, MatchStatus.YET_TO_START.value)

        Match.play_match(user_id=self.user1_id, match_id=self.match1_id)

        match = Match.objects.get(user_id=self.user1_id, match_id=self.match1_id)
        self.assertEqual(match.status, MatchStatus.IN_PROGRESS.value)
