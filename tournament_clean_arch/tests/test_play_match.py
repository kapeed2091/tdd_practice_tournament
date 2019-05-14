from unittest import TestCase
from mock import Mock


class TestPlayMatch(TestCase):
    def test_play_match(self):
        user_id = 1
        round_number = 3
        match_id = 1
        user_match_id = 1
        tournament_id = 1

        storage = Mock()
        presenter = Mock()

        storage.get_tournament.return_value = self.get_tournament_details()
        storage.get_unassigned_match_for_round.return_value = match_id
        storage.assign_match_to_user.return_value = user_match_id

        presenter_response = {"user_match_id": user_match_id}
        presenter.present_play_match.return_value = presenter_response

        from tournament_clean_arch.use_cases.play_match_interactor \
            import PlayMatchInteractor
        use_case = PlayMatchInteractor(storage=storage, presenter=presenter)

        use_case.setup(
            user_id=user_id, round_number=round_number,
            tournament_id=tournament_id
        )

        use_case_response = use_case.execute()
        self.assertEqual(use_case_response, presenter_response)

        self.assertTrue(storage.get_unassigned_match_for_round.called)
        args_dict = storage.get_unassigned_match_for_round.call_args[1]
        self.assertEqual(tournament_id, args_dict.get("tournament_id"))
        self.assertEqual(round_number, args_dict.get("round_number"))

        self.assertTrue(storage.assign_match_to_user.called)
        args_dict = storage.assign_match_to_user.call_args[1]
        self.assertEqual(user_id, args_dict["user_id"])
        self.assertEqual(match_id, args_dict["match_id"])

        self.assertTrue(presenter.present_play_match.called)
        args_dict = presenter.present_play_match.call_args[1]
        self.assertEqual(user_match_id, args_dict["user_match_id"])

    def test_case_invalid_round_number(self):
        user_id = 1
        round_number = 5
        tournament_id = 1

        storage = Mock()
        presenter = Mock()

        storage.get_tournament.return_value = self.get_tournament_details()

        from tournament_clean_arch.use_cases.play_match_interactor \
            import PlayMatchInteractor
        use_case = PlayMatchInteractor(storage=storage, presenter=presenter)

        use_case.setup(
            user_id=user_id, round_number=round_number,
            tournament_id=tournament_id
        )

        from tournament_clean_arch.exceptions.custom_exceptions import \
            InvalidRoundNumber
        with self.assertRaises(InvalidRoundNumber):
            use_case.execute()

        self.assertFalse(storage.get_unassigned_match_for_round.called)
        self.assertFalse(storage.assign_match_to_user.called)
        self.assertFalse(presenter.present_play_match.called)

    def test_case_tournament_is_completed(self):
        user_id = 1
        round_number = 3
        tournament_id = 1

        storage = Mock()
        presenter = Mock()

        storage.get_tournament.return_value = \
            self.get_tournament_details_which_is_completed()

        from tournament_clean_arch.use_cases.play_match_interactor \
            import PlayMatchInteractor
        use_case = PlayMatchInteractor(storage=storage, presenter=presenter)

        use_case.setup(
            user_id=user_id, round_number=round_number,
            tournament_id=tournament_id
        )

        from tournament_clean_arch.exceptions.custom_exceptions import \
            TournamentIsCompleted
        with self.assertRaises(TournamentIsCompleted):
            use_case.execute()

        self.assertFalse(storage.get_unassigned_match_for_round.called)
        self.assertFalse(storage.assign_match_to_user.called)
        self.assertFalse(presenter.present_play_match.called)

    @staticmethod
    def get_tournament_details():
        import datetime
        tournament_date_time = \
            datetime.datetime.now() - datetime.timedelta(days=1)
        return {
            "tournament_id": 1,
            "no_of_rounds": 4,
            "start_datetime": tournament_date_time,
            "status": "IN_PROGRESS"
        }

    @staticmethod
    def get_tournament_details_which_is_completed():
        import datetime
        tournament_date_time = \
            datetime.datetime.now() - datetime.timedelta(days=1)
        return {
            "tournament_id": 1,
            "no_of_rounds": 4,
            "start_datetime": tournament_date_time,
            "status": "COMPLETED"
        }
