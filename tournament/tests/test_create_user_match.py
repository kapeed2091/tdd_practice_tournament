from django.test import TestCase

from tournament.constants.general import TournamentStatus


class TestCreateUserMatch(TestCase):
    def test_create_user_match(self):
        from tournament.models import UserMatch

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        initial_objects_count = UserMatch.objects.all().count()
        UserMatch.create_user_match(user.id, match.id)
        final_objects_count = UserMatch.objects.all().count()

        objects_newly_created_count = \
            final_objects_count - initial_objects_count

        user_match_exists = UserMatch.objects.filter(
            user_id=user.id,
            match_id=match.id
        ).exists()

        self.assertTrue(user_match_exists)
        self.assertEqual(objects_newly_created_count, 1)

    def test_invalid_match_id(self):
        from tournament.models import UserMatch

        user = self.create_user()
        self.create_tournament(user_id=user.id)

        match_id = 1

        from tournament.exceptions.custom_exceptions import InvalidMatchId
        with self.assertRaises(InvalidMatchId):
            UserMatch.create_user_match(user.id, match_id)

    @staticmethod
    def create_tournament(
            user_id, status=TournamentStatus.IN_PROGRESS.value):
        from tournament.models import Tournament

        total_rounds = 4

        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        start_datetime = get_current_local_date_time()

        tournament = Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime,
            status=status
        )

        return tournament

    @staticmethod
    def create_user():
        from tournament.models import User

        user_name = "John"

        user = User.objects.create(name=user_name)
        return user

    @staticmethod
    def create_match(tournament_id, round_number):
        from tournament.models import Match

        match = Match.objects.create(
            tournament_id=tournament_id,
            round_number=round_number
        )

        return match
