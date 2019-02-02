from django.test import TestCase


class TestCreateMatch(TestCase):

    def test_create_match(self):
        from tournament.models import Match
        tournament_id = 1
        round_number = 3

        initial_objects_count = Match.objects.all().count()
        Match.create_match(tournament_id, round_number)
        final_objects_count = Match.objects.all().count()

        objects_newly_created_count = \
            final_objects_count - initial_objects_count

        match_exists = Match.objects.filter(
            tournament_id=tournament_id,
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
