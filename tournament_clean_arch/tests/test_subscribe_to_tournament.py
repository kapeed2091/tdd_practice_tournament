from unittest import TestCase
from mock import Mock


class TestSubscribeToTournament(TestCase):
    def test_case_subscribe_to_tournament(self):
        user_id = 1
        tournament_id = 2
        user_tournament_id = 1

        storage = Mock()
        presenter = Mock()

        storage.create_user_tournament.return_value = user_tournament_id

        presenter_response = {"subscribe_id": user_tournament_id}
        presenter.present_create_user_tournament.return_value = \
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

        self.assertTrue(storage.create_user_tournament.called)
        args_dict = storage.create_user_tournament.call_args[1]

        self.assertEqual(user_id, args_dict.get("user_id"))
        self.assertEqual(tournament_id, args_dict.get("tournament_id"))

        self.assertTrue(presenter.present_create_user_tournament.called)
        args_dict = presenter.present_create_user_tournament.call_args[1]

        self.assertEqual(
            user_tournament_id, args_dict.get("user_tournament_id"))
