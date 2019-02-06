from .test_utils import TestUtils


class TestGetOpponentProfile(TestUtils):
    def test_get_opponent_profile_successful(self):
        user_1_details = {
            "name": "John-2",
            "age": 14,
            "gender": "MALE"
        }

        user_details = {
            "name": "John-2",
            "age": 14,
            "gender": "MALE"
        }

        opponent_details = {
            "name": "John-3",
            "age": 12,
            "gender": "MALE"
        }
        user = self.create_user_(**user_1_details)
        user_2 = self.create_user_(**user_details)
        user_3 = self.create_user_(**opponent_details)

        tournament = self.create_tournament(user_id=user.id)
        self.create_user_tournament(
            user_id=user_2.id,
            tournament_id=tournament.id,
            round_number=3
        )
        self.create_user_tournament(
            user_id=user_3.id,
            tournament_id=tournament.id,
            round_number=3
        )

        round_number = 3
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        self.create_user_match(user_id=user_2.id, match_id=match.id)
        self.create_user_match(user_id=user_3.id, match_id=match.id)

        from tournaments.models import UserMatch
        response_details = UserMatch.get_opponent_player_details(
            user_id=user_2.id, tournament_id=tournament.id
        )

        self.assertDictEqual(opponent_details, response_details)

    def test_player_status_is_dead(self):
        user_1_details = {
            "name": "John-2",
            "age": 14,
            "gender": "MALE"
        }

        user_details = {
            "name": "John-2",
            "age": 14,
            "gender": "MALE"
        }

        opponent_details = {
            "name": "John-3",
            "age": 12,
            "gender": "MALE"
        }
        user = self.create_user_(**user_1_details)
        user_2 = self.create_user_(**user_details)
        user_3 = self.create_user_(**opponent_details)

        tournament = self.create_tournament(user_id=user.id)

        from tournaments.constants.general import UserTournamentStatus
        self.create_user_tournament(
            user_id=user_2.id,
            tournament_id=tournament.id,
            round_number=3,
            status=UserTournamentStatus.DEAD.value
        )
        self.create_user_tournament(
            user_id=user_3.id,
            tournament_id=tournament.id,
            round_number=3,
            status=UserTournamentStatus.DEAD.value
        )

        round_number = 3
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        self.create_user_match(user_id=user_2.id, match_id=match.id)
        self.create_user_match(user_id=user_3.id, match_id=match.id)

        from tournaments.models import UserMatch

        from tournaments.exceptions.custom_exceptions import \
            UserNotInTournamentAnymore
        with self.assertRaises(UserNotInTournamentAnymore):
            UserMatch.get_opponent_player_details(
                user_id=user_2.id, tournament_id=tournament.id
            )
