from unittest import TestCase
from mock import Mock


class TestSubscribeToTournament(TestCase):
    def test_case_subscribe_to_tournament(self):
        user_id = 1
        tournament_id = 2
        subscribe_id = 1

        storage = Mock()
        presenter = Mock()

        storage.get_tournament.return_value = \
            self.get_details_of_tournament_that_has_not_started()
        storage.subscribe_to_tournament.return_value = subscribe_id

        presenter_response = {"subscribe_id": subscribe_id}
        presenter.present_subscribe_to_tournament.return_value = \
            presenter_response

        from tournament_clean_arch.use_cases. \
            subscribe_to_tournament_interactor import \
            SubscribeToTournamentInteractor
        use_case = SubscribeToTournamentInteractor(
            storage=storage, presenter=presenter)

        use_case.setup(
            user_id=user_id, tournament_id=tournament_id
        )

        use_case_response = use_case.execute()
        self.assertEqual(use_case_response, presenter_response)

        self.assertTrue(storage.subscribe_to_tournament.called)
        args_dict = storage.subscribe_to_tournament.call_args[1]

        self.assertEqual(user_id, args_dict.get("user_id"))
        self.assertEqual(tournament_id, args_dict.get("tournament_id"))

        self.assertTrue(presenter.present_subscribe_to_tournament.called)
        args_dict = presenter.present_subscribe_to_tournament.call_args[1]

        self.assertEqual(subscribe_id, args_dict.get("subscribe_id"))

    def test_case_tournament_already_started(self):
        user_id = 1
        tournament_id = 2

        storage = Mock()
        presenter = Mock()

        storage.get_tournament.return_value = \
            self.get_details_of_tournament_that_has_started()

        from tournament_clean_arch.use_cases. \
            subscribe_to_tournament_interactor import \
            SubscribeToTournamentInteractor
        use_case = SubscribeToTournamentInteractor(
            storage=storage, presenter=presenter)

        use_case.setup(
            user_id=user_id, tournament_id=tournament_id
        )

        from tournament_clean_arch.exceptions.custom_exceptions import \
            TournamentHasStarted
        with self.assertRaises(TournamentHasStarted):
            use_case.execute()

        self.assertFalse(storage.subscribe_to_tournament.called)
        self.assertFalse(presenter.present_subscribe_to_tournament.called)

    def test_case_tournament_is_full(self):
        user_id = 1
        tournament_id = 2

        storage = Mock()
        presenter = Mock()

        storage.get_tournament.return_value = \
            self.get_details_of_tournament_that_has_not_started()
        storage.get_total_subscribers_for_tournament.return_value = \
            self.get_total_subscribers_for_completely_filled_tournament()

        from tournament_clean_arch.use_cases. \
            subscribe_to_tournament_interactor import \
            SubscribeToTournamentInteractor
        use_case = SubscribeToTournamentInteractor(
            storage=storage, presenter=presenter)

        use_case.setup(
            user_id=user_id, tournament_id=tournament_id
        )

        from tournament_clean_arch.exceptions.custom_exceptions import \
            TournamentIsFull
        with self.assertRaises(TournamentIsFull):
            use_case.execute()

        self.assertFalse(storage.subscribe_to_tournament.called)
        self.assertFalse(presenter.present_subscribe_to_tournament.called)

    @staticmethod
    def get_details_of_tournament_that_has_started():
        import datetime
        tournament_date_time = \
            datetime.datetime.now() - datetime.timedelta(days=1)
        return {
            "tournament_id": 1,
            "no_of_rounds": 4,
            "start_datetime": tournament_date_time
        }

    @staticmethod
    def get_details_of_tournament_that_has_not_started():
        import datetime
        tournament_date_time = \
            datetime.datetime.now() + datetime.timedelta(days=1)
        return {
            "tournament_id": 1,
            "no_of_rounds": 4,
            "start_datetime": tournament_date_time
        }

    @staticmethod
    def get_total_subscribers_for_completely_filled_tournament():
        return 16
