from .test_utils import TestUtils


class TestLevelUp(TestUtils):

    def test_level_up(self):
        user_1 = self.create_user()
        user_2 = self.create_user(name="John-2")

        tournament = self.create_tournament(user_id=user_1.id)

        self.create_user_tournament(
            user_id=user_1.id, tournament_id=tournament.id
        )
        self.create_user_tournament(
            user_id=user_2.id, tournament_id=tournament.id
        )

        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        self.create_user_match(
            user_id=user_1.id, match_id=match.id, score=100
        )

        self.create_user_match(
            user_id=user_2.id, match_id=match.id, score=200
        )

        from tournaments.models import UserTournament
        UserTournament.level_up(
            user_id=user_2.id, match_id=match.id
        )

        player = UserTournament.objects.get(
            user_id=user_2.id, tournament_id=tournament.id
        )

        self.assertEqual(player.round_number, round_number + 1)
