from .test_utils import TestUtils


class TestSubmitScore(TestUtils):
    def test_submit_score(self):
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

        user_match = self.create_user_match(
            user_id=user.id, match_id=match.id
        )

        score = 200
        user_match.submit_score(score=score)

        user_match_obj = UserMatch.objects.get(
            user_id=user.id, match_id=match.id
        )
        self.assertEqual(user_match_obj.score, score)

    def test_invalid_score(self):
        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )
        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        user_match = self.create_user_match(
            user_id=user.id, match_id=match.id
        )

        score = -100

        from tournaments.exceptions.custom_exceptions import InvalidScore
        with self.assertRaises(InvalidScore):
            user_match.submit_score(score=score)
