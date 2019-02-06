from django.test import TestCase
from django_swagger_utils.drf_server.exceptions import NotFound
from ib_common.date_time_utils.get_current_datetime import get_current_datetime
import datetime

from tournament.constants.general import TournamentStatus, MatchStatus, MatchUserStatus


class TestGetUserCurrentRound(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    invalid_user_id = 'InvalidUser'
    match1_id = 'Match1'
    match2_id = 'Match2'

    def setUp(self):
        from tournament.models import User, Match, KoTournament

        user1 = User.objects.create(
            user_id=self.user1_id
        )

        now = get_current_datetime()
        tournament1 = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament1',
            no_of_rounds=3,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )

        Match.objects.create(
            match_id=self.match2_id,
            user=user1,
            tournament=tournament1,
            round=2,
            status=MatchStatus.YET_TO_START.value,
            user_status=MatchUserStatus.NOT_DECIDED_YET.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user1,
            tournament=tournament1,
            round=1,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.WIN.value
        )

    def test_get_user_current_round(self):
        from tournament.models import KoTournament

        current_round = KoTournament.get_user_current_round(
            user_id=self.user1_id, tournament_id=1)

        self.assertEqual(current_round, 2)

    def test_get_user_current_round_invalid_user(self):
        from tournament.models import KoTournament

        with self.assertRaisesMessage(NotFound, 'Invalid user id'):
            KoTournament.get_user_current_round(
                user_id=self.invalid_user_id, tournament_id=1)
