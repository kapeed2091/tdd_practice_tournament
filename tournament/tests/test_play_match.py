from django.test import TestCase
from django_swagger_utils.drf_server.exceptions import Forbidden, NotFound
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

import datetime

from tournament.constants.general import TournamentStatus, MatchStatus


class TestPlayMatch(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    user2_id = 'User2'
    invalid_user_id = 'InvalidUser'
    match1_id = 'Match1'
    match2_id = 'Match2'
    invalid_match_id = 'InvalidMatch'

    def setUp(self):
        from tournament.models import User, KoTournament, Match

        now = get_current_datetime()
        user1 = User.objects.create(
            user_id=self.user1_id
        )

        User.objects.create(
            user_id=self.user2_id
        )

        tournament1 = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament1',
            no_of_rounds=2,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )

        tournament2 = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament2',
            no_of_rounds=2,
            start_datetime=now + datetime.timedelta(days=1),
            status=TournamentStatus.YET_TO_START.value
        )

        Match.objects.create(
            match_id=self.match1_id,
            user=user1,
            tournament=tournament1,
            status=MatchStatus.YET_TO_START.value
        )

        Match.objects.create(
            match_id=self.match2_id,
            user=user1,
            tournament=tournament2,
            status=MatchStatus.YET_TO_START.value
        )

    def test_user_will_play_match(self):
        from tournament.models import User, Match

        user1 = User.objects.get(user_id=self.user1_id)
        match_before = Match.objects.get(user=user1, match_id=self.match1_id)
        self.assertEqual(match_before.status, MatchStatus.YET_TO_START.value)

        Match.play_match(user_id=self.user1_id, match_id=self.match1_id)

        match = Match.objects.get(user=user1, match_id=self.match1_id)
        self.assertEqual(match.status, MatchStatus.IN_PROGRESS.value)

    def test_user_try_to_play_match_where_tournament_is_not_started(self):
        from tournament.models import Match

        with self.assertRaisesMessage(Forbidden, 'Match can be played only after the tournament has started'):
            Match.play_match(user_id=self.user1_id, match_id=self.match2_id)

    def test_play_match_with_invalid_user(self):
        from tournament.models import Match

        with self.assertRaisesMessage(NotFound, 'User does not exist with the given user id'):
            Match.play_match(user_id=self.invalid_user_id, match_id=self.match2_id)

    def test_play_match_with_invalid_match_id(self):
        from tournament.models import Match

        with self.assertRaisesMessage(NotFound, 'Match does not exist with the given match id'):
            Match.play_match(user_id=self.user1_id, match_id=self.invalid_match_id)

    def test_play_match_user_does_not_belong_to_match(self):
        from tournament.models import Match

        with self.assertRaisesMessage(Forbidden, 'User does not belong to the match'):
            Match.play_match(user_id=self.user2_id, match_id=self.match1_id)
