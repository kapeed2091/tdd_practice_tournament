from .test_utils import TestUtils


class TestUpdateLoserStatus(TestUtils):

    def test_update_loser_status_successful(self):
        user_1 = self.create_user()
        user_2 = self.create_user(name="John-2")

        tournament = self.create_tournament(user_id=user_1.id)

        player_1 = self.create_user_tournament(
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

        from tournaments.constants.general import UserTournamentStatus
        self.assertEqual(player_1.status, UserTournamentStatus.ALIVE.value)

        from tournaments.models import UserTournament
        UserTournament.update_loser_status(match_id=match.id)

        player_1 = UserTournament.objects.get(
            user_id=user_1.id, tournament_id=tournament.id
        )
        self.assertEqual(player_1.status, UserTournamentStatus.DEAD.value)

    def test_re_updating_loser_status(self):
        user_1 = self.create_user()
        user_2 = self.create_user(name="John-2")

        tournament = self.create_tournament(user_id=user_1.id)

        from tournaments.constants.general import UserTournamentStatus
        player_1 = self.create_user_tournament(
            user_id=user_1.id, tournament_id=tournament.id,
            status=UserTournamentStatus.DEAD.value
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
        from tournaments.exceptions.custom_exceptions import \
            LoserStatusAlreadyUpdated
        with self.assertRaises(LoserStatusAlreadyUpdated):
            UserTournament.update_loser_status(match_id=match.id)
