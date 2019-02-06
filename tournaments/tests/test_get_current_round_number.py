from .test_utils import TestUtils


class TestGetCurrentRoundNumber(TestUtils):

    def test_get_current_round_number_successful(self):
        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        user_tournament = self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )

        from tournaments.models import UserTournament
        round_number = UserTournament.get_current_round_number(
            user_id=user.id, tournament_id=tournament.id
        )

        self.assertEqual(user_tournament.round_number, round_number)
