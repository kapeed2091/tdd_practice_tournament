from django.test import TestCase
from django_swagger_utils.drf_server.exceptions import NotFound
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

import datetime

from tournament.constants.general import TournamentStatus, MatchStatus, MatchUserStatus


class TestGetTournamentWinnerProfile(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    user2_id = 'User2'
    user3_id = 'User3'
    user4_id = 'User4'
    invalid_user_id = 'InvalidUser'
    user1_dict = {
        'user_id': user1_id,
        'name': 'Name1',
        'age': 10,
        'gender': 'Female'
    }
    user2_dict = {
        'user_id': user2_id,
        'name': 'Name2',
        'age': 20,
        'gender': 'Male'
    }
    user3_dict = {
        'user_id': user3_id,
        'name': 'Name3',
        'age': 15,
        'gender': 'Male'
    }
    user4_dict = {
        'user_id': user4_id,
        'name': 'Name4',
        'age': 30,
        'gender': 'Female'
    }
    match1_id = 'Match1'
    match2_id = 'Match2'

    def test_get_tournament_winner_profile(self):
        from tournament.models import KoTournament

        self.setup_get_tournament_winner_profile()
        winner = KoTournament.get_winner_profile(tournament_id=1)
        expected_winner = self.user1_dict
        expected_winner.pop('user_id')
        self.assertEqual(expected_winner, winner)

    def setup_get_tournament_winner_profile(self):
        self.create_tournament_and_matches(
            tournament_name='Tournament1',
            win_user_dict=self.user1_dict,
            lost_user_dict=self.user2_dict
        )

        self.create_tournament_and_matches(
            tournament_name='Tournament2',
            win_user_dict=self.user3_dict,
            lost_user_dict=self.user4_dict
        )

    def create_tournament_and_matches(self, tournament_name, win_user_dict, lost_user_dict):
        from tournament.models import User, Match, KoTournament
        user1 = User.objects.create(**win_user_dict)
        user2 = User.objects.create(**lost_user_dict)

        now = get_current_datetime()
        tournament1 = KoTournament.objects.create(
            created_user_id=self.user_id,
            name=tournament_name,
            no_of_rounds=3,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.COMPLETED.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user1,
            tournament=tournament1,
            round=3,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.WIN.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user2,
            tournament=tournament1,
            round=3,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.LOST.value
        )

    def test_winner_is_not_declared_yet(self):
        from tournament.models import KoTournament

        self.setup_winner_is_not_declared_yet()
        with self.assertRaisesMessage(NotFound, 'Winner is not declared yet'):
            KoTournament.get_winner_profile(tournament_id=1)

    def setup_winner_is_not_declared_yet(self):
        from tournament.models import User, Match, KoTournament

        user1 = User.objects.create(**self.user1_dict)
        user2 = User.objects.create(**self.user2_dict)
        now = get_current_datetime()
        tournament1 = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament1',
            no_of_rounds=3,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.COMPLETED.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user1,
            tournament=tournament1,
            round=3,
            status=MatchStatus.YET_TO_START.value,
            user_status=MatchUserStatus.NOT_DECIDED_YET.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user2,
            tournament=tournament1,
            round=3,
            status=MatchStatus.YET_TO_START.value,
            user_status=MatchUserStatus.NOT_DECIDED_YET.value
        )

    def test_invalid_user_id(self):
        from tournament.models import KoTournament

        self.setup_invalid_user_id()
        with self.assertRaisesMessage(NotFound, 'Invalid user id'):
            KoTournament.get_winner_profile(user_id=self.invalid_user_id, tournament_id=1)

    def setup_invalid_user_id(self):
        self.create_tournament_and_matches(
            tournament_name='Tournament1',
            win_user_dict=self.user1_dict,
            lost_user_dict=self.user2_dict
        )

        self.create_tournament_and_matches(
            tournament_name='Tournament2',
            win_user_dict=self.user3_dict,
            lost_user_dict=self.user4_dict
        )
