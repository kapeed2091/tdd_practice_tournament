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
            UserMatch.create_user_match(user_id, match.id)

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
