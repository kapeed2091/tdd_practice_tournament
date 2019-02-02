from django.test import TestCase

from tournaments.constants.general import TournamentStatus
from .test_utils import TestUtils


class TestCreateMatch(TestUtils):

    def test_create_match(self):
        from tournaments.models import Match

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
        from tournaments.models import Match
        tournament_id = 1
        round_number = 3

        from tournaments.exceptions.custom_exceptions import \
            InvalidTournamentId
        with self.assertRaises(InvalidTournamentId):
            Match.create_match(tournament_id, round_number)

    def test_negative_round_number(self):
        from tournaments.models import Match

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        round_number = -3

        from tournaments.exceptions.custom_exceptions import InvalidRoundNumber
        with self.assertRaises(InvalidRoundNumber):
            Match.create_match(tournament.id, round_number)
