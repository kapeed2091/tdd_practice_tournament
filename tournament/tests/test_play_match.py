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

    def test_user_will_play_match(self):
        self.setup_user_will_play_match()

        from tournament.models import User, Match

        user1 = User.objects.get(user_id=self.user1_id)
        match_before = Match.objects.get(user=user1, match_id=self.match1_id)
        self.assertEqual(match_before.status, MatchStatus.YET_TO_START.value)

        Match.play_match(user_id=self.user1_id, match_id=self.match1_id)

        match = Match.objects.get(user=user1, match_id=self.match1_id)
        self.assertEqual(match.status, MatchStatus.IN_PROGRESS.value)

    def setup_user_will_play_match(self):
        self.create_user_tournament_match(
            user_id=self.user1_id,
            tournament_status=TournamentStatus.IN_PROGRESS.value,
            match_id=self.match1_id
        )

    def test_user_try_to_play_match_where_tournament_is_not_started(self):
        self.setup_user_try_to_play_match_where_tournament_is_not_started()

        from tournament.models import Match

        with self.assertRaisesMessage(Forbidden, 'Match can be played only after the tournament has started'):
            Match.play_match(user_id=self.user1_id, match_id=self.match2_id)

    def setup_user_try_to_play_match_where_tournament_is_not_started(self):
        self.create_user_tournament_match(
            user_id=self.user1_id,
            tournament_status=TournamentStatus.YET_TO_START.value,
            match_id=self.match2_id
        )

    def test_play_match_with_invalid_user(self):
        from tournament.models import Match

        with self.assertRaisesMessage(NotFound, 'User does not exist with the given user id'):
            Match.play_match(user_id=self.invalid_user_id, match_id=self.match2_id)

    def test_play_match_with_invalid_match_id(self):
        self.setup_play_match_with_invalid_match_id()

        from tournament.models import Match

        with self.assertRaisesMessage(NotFound, 'Match does not exist with the given match id'):
            Match.play_match(user_id=self.user1_id, match_id=self.invalid_match_id)

    def setup_play_match_with_invalid_match_id(self):
        from tournament.models import User

        User.objects.create(
            user_id=self.user1_id
        )

    def test_play_match_user_does_not_belong_to_match(self):
        self.setup_play_match_user_does_not_belong_to_match()

        from tournament.models import Match

        with self.assertRaisesMessage(Forbidden, 'User does not belong to the match'):
            Match.play_match(user_id=self.user2_id, match_id=self.match1_id)

    def setup_play_match_user_does_not_belong_to_match(self):
        self.create_user_tournament_match(
            user_id=self.user1_id,
            tournament_status=TournamentStatus.IN_PROGRESS.value,
            match_id=self.match1_id
        )

        from tournament.models import User
        User.objects.create(
            user_id=self.user2_id
        )

    def create_user_tournament_match(self, user_id, tournament_status, match_id):
        from tournament.models import User, KoTournament, Match

        now = get_current_datetime()
        user = User.objects.create(
            user_id=user_id
        )
        tournament = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament',
            no_of_rounds=2,
            start_datetime=now + datetime.timedelta(days=1),
            status=tournament_status
        )
        Match.objects.create(
            match_id=match_id,
            user=user,
            tournament=tournament,
            status=MatchStatus.YET_TO_START.value
        )
