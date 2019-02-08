from tournaments.constants.general import UserTournamentStatus
from .test_utils import TestUtils


class TestCreateUserMatch(TestUtils):
    def test_create_user_match(self):
        from tournaments.models import UserMatch

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )
        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        initial_objects_count = UserMatch.objects.all().count()
        UserMatch.create_user_match(
            user_id=user.id, match_id=match.id
        )
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
        from tournaments.models import UserMatch

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)
        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )

        match_id = 1

        from tournaments.exceptions.custom_exceptions import InvalidMatchId
        with self.assertRaises(InvalidMatchId):
            UserMatch.create_user_match(
                user_id=user.id, match_id=match_id
            )

    def test_invalid_user_id(self):
        from tournaments.models import UserMatch
        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)
        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )
        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        user_id = 2

        from tournaments.exceptions.custom_exceptions import InvalidUserId
        with self.assertRaises(InvalidUserId):
            UserMatch.create_user_match(
                user_id=user_id, match_id=match.id
            )

    def test_user_not_in_tournament(self):
        from tournaments.models import UserMatch
        user = self.create_user()
        user_2 = self.create_user(name="John_2")

        tournament = self.create_tournament(user_id=user.id)

        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        from tournaments.exceptions.custom_exceptions import \
            UserNotInTournament
        with self.assertRaises(UserNotInTournament):
            UserMatch.create_user_match(
                user_id=user_2.id, match_id=match.id
            )

    def test_user_playing_wrong_match(self):
        from tournaments.models import UserMatch

        user_1 = self.create_user()
        tournament = self.create_tournament(user_id=user_1.id)
        self.create_user_tournament(
            user_id=user_1.id, tournament_id=tournament.id
        )

        user_2 = self.create_user("John-2")
        self.create_user_tournament(
            user_id=user_2.id, tournament_id=tournament.id
        )

        match = self.create_match(tournament_id=tournament.id, round_number=1)
        self.create_user_match(user_id=user_1.id, match_id=match.id)
        self.create_user_match(user_id=user_2.id, match_id=match.id)

        user_3 = self.create_user("John-3")
        self.create_user_tournament(
            user_id=user_3.id, tournament_id=tournament.id
        )

        from tournaments.exceptions.custom_exceptions import MatchIdOverused
        with self.assertRaises(MatchIdOverused):
            UserMatch.create_user_match(
                user_id=user_3.id, match_id=match.id
            )

    def test_user_is_in_dead_state(self):
        from tournaments.models import UserMatch

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id,
            status=UserTournamentStatus.DEAD.value
        )
        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        from tournaments.exceptions.custom_exceptions import \
            UserNotInTournamentAnymore
        with self.assertRaises(UserNotInTournamentAnymore):
            UserMatch.create_user_match(
                user_id=user.id, match_id=match.id
            )

    def test_all_players_are_not_present_in_round(self):
        from tournaments.models import UserMatch

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id,
            round_number=2
        )
        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        from tournaments.exceptions.custom_exceptions import \
            InsufficientMembersInRoundToPlayMatch
        with self.assertRaises(InsufficientMembersInRoundToPlayMatch):
            UserMatch.create_user_match(
                user_id=user.id, match_id=match.id
            )
