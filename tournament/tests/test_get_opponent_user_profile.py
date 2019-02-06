from django.test import TestCase
from ib_common.date_time_utils.get_current_datetime import get_current_datetime
import datetime

from tournament.constants.general import TournamentStatus, MatchStatus, MatchUserStatus


class TestGetOpponentUserProfile(TestCase):

    user_id = 'User'
    user_dict = {
        'user_id': 'User1',
        'name': 'Name1',
        'age': 10,
        'gender': 'Female'
    }
    opponent_user_dict = {
        'user_id': 'User2',
        'name': 'Name2',
        'age': 20,
        'gender': 'Male'
    }
    match_id = 'Match'

    def setUp(self):
        from tournament.models import User, Match, KoTournament
        user = User.objects.create(**self.user_dict)
        opponent_user = User.objects.create(**self.opponent_user_dict)

        now = get_current_datetime()
        tournament = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament',
            no_of_rounds=3,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )

        Match.objects.create(
            match_id=self.match_id,
            user=user,
            tournament=tournament,
            round=2,
            status=MatchStatus.YET_TO_START.value,
            user_status=MatchUserStatus.NOT_DECIDED_YET.value
        )
        Match.objects.create(
            match_id=self.match_id,
            user=opponent_user,
            tournament=tournament,
            round=2,
            status=MatchStatus.YET_TO_START.value,
            user_status=MatchUserStatus.NOT_DECIDED_YET.value
        )

    def test_get_opponent_user_profile(self):
        from tournament.models import KoTournament

        opponent_user = KoTournament.get_opponent_user_profile(
            tournament_round=2, tournament_id=1)
        self.assertEqual(self.opponent_user_dict, opponent_user)
