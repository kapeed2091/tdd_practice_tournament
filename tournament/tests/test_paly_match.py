import datetime
from django.test import TestCase
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

from tournament.constants.general import TournamentStatus, MatchStatus


class TestPlayMatch(TestCase):

    user1_id = 'User1'

    def setUp(self):
        from tournament.models import Match, KoTournament, User

        now = get_current_datetime()
        User.objects.create(user_id='User')
        user1 = User.objects.create(user_id=self.user1_id)
        tournament = KoTournament.objects.create(
            created_user_id='User',
            name='Tournament1',
            no_of_rounds=2,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )
        Match.objects.create(
            user=user1,
            tournament=tournament,
            status=MatchStatus.YET_TO_START.value
        )

    def test_play_match(self):
        from tournament.models import Match, User

        Match.play_match(user_id=self.user1_id, match_id=1)

        user1 = User.objects.get(user_id=self.user1_id)
        match = Match.objects.get(user=user1)
        self.assertEqual(match.status, MatchStatus.IN_PROGRESS.value)
