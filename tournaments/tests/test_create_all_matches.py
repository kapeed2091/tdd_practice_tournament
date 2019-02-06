from .test_utils import TestUtils


class TestCreateAllMatchesForTournament(TestUtils):
    def test_create_all_matches_successful(self):
        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)
        total_rounds = tournament.total_rounds

        from tournaments.models import Match
        initial_objects_count = Match.objects.filter(
            tournament_id=tournament.id).count()
        Match.create_all_matches(tournament_id=tournament.id)
        final_objects_count = Match.objects.filter(
            tournament_id=tournament.id).count()

        self.assertEqual(0, initial_objects_count)
        self.assertEqual((2 ** total_rounds) - 1, final_objects_count)
