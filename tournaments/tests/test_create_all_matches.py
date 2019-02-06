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

    def test_invalid_tournament_id(self):
        self.create_user()

        tournament_id = 1

        from tournaments.models import Match

        from tournaments.exceptions.custom_exceptions import \
            InvalidTournamentId
        with self.assertRaises(InvalidTournamentId):
            Match.create_all_matches(tournament_id=tournament_id)

    def test_re_creating_matches(self):
        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        self.create_tournament_matches(
            tournament_id=tournament.id, total_rounds=tournament.total_rounds
        )

        from tournaments.models import Match

        from tournaments.exceptions.custom_exceptions import \
            TournamentMatchesAlreadyExist
        with self.assertRaises(TournamentMatchesAlreadyExist):
            Match.create_all_matches(tournament_id=tournament.id)
