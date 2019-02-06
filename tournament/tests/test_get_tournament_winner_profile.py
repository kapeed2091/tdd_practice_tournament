from django.test import TestCase
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

import datetime

from tournament.constants.general import TournamentStatus, MatchStatus, MatchUserStatus


class TestGetTournamentWinnerProfile(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    user2_id = 'User2'
    user3_id = 'User3'
    user4_id = 'User4'
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

    def setUp(self):
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

        user3 = User.objects.create(**self.user3_dict)
        user4 = User.objects.create(**self.user4_dict)
        tournament2 = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament2',
            no_of_rounds=3,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.COMPLETED.value
        )
        Match.objects.create(
            match_id=self.match2_id,
            user=user3,
            tournament=tournament2,
            round=3,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.WIN.value
        )
        Match.objects.create(
            match_id=self.match2_id,
            user=user4,
            tournament=tournament2,
            round=3,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.LOST.value
        )

    def test_get_tournament_winner_profile(self):
        from tournament.models import KoTournament

        winner = KoTournament.get_winner_profile(tournament_id=1)
        expected_winner = self.user1_dict
        expected_winner.pop('user_id')
        self.assertEqual(expected_winner, winner)
