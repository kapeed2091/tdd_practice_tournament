from .test_utils import TestUtils


class TestGetWinnerProfile(TestUtils):
    def test_get_winner_profile_successful(self):
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

        from tournaments.constants.general import UserTournamentStatus
        tournament = self.create_tournament(user_id=user.id)
        self.create_user_tournament(
            user_id=user_2.id,
            tournament_id=tournament.id,
            round_number=4
        )
        self.create_user_tournament(
            user_id=user_3.id,
            tournament_id=tournament.id,
            status=UserTournamentStatus.DEAD.value,
            round_number=4
        )

        round_number = 4
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        self.create_user_match(
            user_id=user_2.id, match_id=match.id, score=300
        )
        self.create_user_match(
            user_id=user_3.id, match_id=match.id, score=200
        )

        from tournaments.models import User

        response_details = User.get_winner_profile(
            tournament_id=tournament.id
        )

        self.assertDictEqual(user_details, response_details)

    def test_tournament_is_in_progress(self):
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
            round_number=4
        )
        self.create_user_tournament(
            user_id=user_3.id,
            tournament_id=tournament.id,
            round_number=4
        )

        round_number = 4
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        self.create_user_match(
            user_id=user_2.id, match_id=match.id, score=300
        )
        self.create_user_match(
            user_id=user_3.id, match_id=match.id, score=200
        )

        from tournaments.models import User

        from tournaments.exceptions.custom_exceptions import \
            TournamentInProgress
        with self.assertRaises(TournamentInProgress):
            User.get_winner_profile(
                tournament_id=tournament.id
            )

    def test_get_winner_profile_successful_(self):
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

        from tournaments.constants.general import UserTournamentStatus, \
            TournamentStatus
        tournament = self.create_tournament(
            user_id=user.id,
            status=TournamentStatus.COMPLETED.value
        )
        self.create_user_tournament(
            user_id=user_2.id,
            tournament_id=tournament.id,
            round_number=4
        )
        self.create_user_tournament(
            user_id=user_3.id,
            tournament_id=tournament.id,
            status=UserTournamentStatus.DEAD.value,
            round_number=4
        )

        round_number = 4
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        self.create_user_match(
            user_id=user_2.id, match_id=match.id, score=300
        )
        self.create_user_match(
            user_id=user_3.id, match_id=match.id, score=200
        )

        from tournaments.models import User

        response_details = User.get_winner_profile(
            tournament_id=tournament.id
        )

        self.assertDictEqual(user_details, response_details)
