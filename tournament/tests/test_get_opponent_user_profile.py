from django.test import TestCase
from django_swagger_utils.drf_server.exceptions import NotFound
from ib_common.date_time_utils.get_current_datetime import get_current_datetime
import datetime

from tournament.constants.general import TournamentStatus, MatchStatus, MatchUserStatus


class TestGetOpponentUserProfile(TestCase):
    user_id = 'User'
    user1_id = 'User1'
    user2_id = 'User2'
    invalid_user_id = 'InvalidUser'
    user_dict = {
        'user_id': user1_id,
        'name': 'Name1',
        'age': 10,
        'gender': 'Female'
    }
    opponent_user_dict = {
        'user_id': user2_id,
        'name': 'Name2',
        'age': 20,
        'gender': 'Male'
    }
    match_id = 'Match'

    def setup_create_tournament(self):
        from tournament.models import KoTournament

        now = get_current_datetime()
        tournament = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament',
            no_of_rounds=3,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )
        return tournament

    @staticmethod
    def setup_assign_user_match(user, match_id, tournament):
        from tournament.models import Match

        Match.objects.create(
            match_id=match_id,
            user=user,
            tournament=tournament,
            round=2,
            status=MatchStatus.YET_TO_START.value,
            user_status=MatchUserStatus.NOT_DECIDED_YET.value
        )

    def test_get_opponent_user_profile(self):
        from tournament.models import KoTournament

        self.setup_get_opponent_user_profile()
        expected_opponent = self.opponent_user_dict
        expected_opponent.pop('user_id')
        opponent_user = KoTournament.get_opponent_user_profile(
            user_id=self.user1_id, tournament_round=2, tournament_id=1)
        self.assertEqual(expected_opponent, opponent_user)

    def setup_get_opponent_user_profile(self):
        from tournament.models import User

        tournament = self.setup_create_tournament()
        user = User.objects.create(**self.user_dict)
        self.setup_assign_user_match(
            user=user, match_id=self.match_id, tournament=tournament)

        opponent_user = User.objects.create(**self.opponent_user_dict)
        self.setup_assign_user_match(
            user=opponent_user, match_id=self.match_id, tournament=tournament)

    def test_get_opponent_user_profile_where_opponent_is_not_yet_assigned(self):
        from tournament.models import KoTournament

        self.setup_get_opponent_user_profile_where_opponent_is_not_yet_assigned()
        with self.assertRaisesMessage(NotFound, 'Opponent is not yet assigned'):
            KoTournament.get_opponent_user_profile(
                user_id=self.user1_id, tournament_round=2, tournament_id=1)

    def setup_get_opponent_user_profile_where_opponent_is_not_yet_assigned(self):
        from tournament.models import User

        tournament = self.setup_create_tournament()
        user = User.objects.create(**self.user_dict)
        self.setup_assign_user_match(
            user=user, match_id=self.match_id, tournament=tournament)

        # There is no opponent yet assigned to the match
        self.setup_assign_user_match(
            user=None, match_id=self.match_id, tournament=tournament
        )

    def test_user_has_no_match_in_the_given_round(self):
        from tournament.models import KoTournament

        self.setup_user_has_no_match_in_the_given_round()
        with self.assertRaisesMessage(NotFound, 'User has no match in the given round'):
            KoTournament.get_opponent_user_profile(
                user_id=self.user1_id, tournament_round=2, tournament_id=1)

    def setup_user_has_no_match_in_the_given_round(self):
        from tournament.models import User

        tournament = self.setup_create_tournament()
        User.objects.create(**self.user_dict)
        opponent_user = User.objects.create(**self.opponent_user_dict)
        self.setup_assign_user_match(
            user=opponent_user, match_id=self.match_id, tournament=tournament)

    def test_invalid_user_id(self):
        from tournament.models import KoTournament

        self.setup_invalid_user_id()
        with self.assertRaisesMessage(NotFound, 'Invalid user id'):
            KoTournament.get_opponent_user_profile(
                user_id=self.invalid_user_id, tournament_round=2, tournament_id=1)

    def setup_invalid_user_id(self):
        from tournament.models import User

        tournament = self.setup_create_tournament()
        user = User.objects.create(**self.user_dict)
        self.setup_assign_user_match(
            user=user, match_id=self.match_id, tournament=tournament)

        opponent_user = User.objects.create(**self.opponent_user_dict)
        self.setup_assign_user_match(
            user=opponent_user, match_id=self.match_id, tournament=tournament)

    def test_invalid_tournament_id(self):
        from tournament.models import KoTournament

        self.setup_invalid_tournament_id()
        with self.assertRaisesMessage(NotFound, 'Tournament does not exist with the given tournament id'):
            KoTournament.get_opponent_user_profile(
                user_id=self.user1_id, tournament_round=2, tournament_id=3)

    def setup_invalid_tournament_id(self):
        from tournament.models import User

        self.setup_create_tournament()
        User.objects.create(**self.user_dict)
