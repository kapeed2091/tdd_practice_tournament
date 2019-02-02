from django.test import TestCase

from tournament.constants.general import TournamentStatus


class TestCreateMatch(TestCase):

    def test_create_match(self):
        from tournament.models import Match

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        round_number = 3

        initial_objects_count = Match.objects.all().count()
        Match.create_match(tournament.id, round_number)
        final_objects_count = Match.objects.all().count()

        objects_newly_created_count = \
            final_objects_count - initial_objects_count

        match_exists = Match.objects.filter(
            tournament_id=tournament.id,
            round_number=round_number
        ).exists()

        self.assertTrue(match_exists)
        self.assertEqual(objects_newly_created_count, 1)

    def test_invalid_tournament(self):
        from tournament.models import Match
        tournament_id = 1
        round_number = 3

        from tournament.exceptions.custom_exceptions import InvalidTournamentId
        with self.assertRaises(InvalidTournamentId):
            Match.create_match(tournament_id, round_number)

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
