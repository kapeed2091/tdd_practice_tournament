import datetime
from unittest import TestCase
from mock import Mock
import copy


class TestCreateTournament(TestCase):
    def test_create_tournament(self):
        tournament_date_time = \
            datetime.datetime.now() + datetime.timedelta(days=1)
        tournament_data = {
            "tournament_id": 1,
            "no_of_rounds": 4,
            "start_datetime":
                tournament_date_time.strftime("%m/%d/%Y, %H:%M:%S")
        }
        tournament_data_with_date_as_obj = copy.deepcopy(tournament_data)
        tournament_data_with_date_as_obj["start_datetime"] = \
            tournament_date_time

        storage = Mock()
        presenter = Mock()

        tournament_id = tournament_data["tournament_id"]
        storage.create_tournament.return_value = tournament_id
        storage.get_tournament.return_value = tournament_data_with_date_as_obj
        presenter.present_create_tournament.return_value = tournament_data

        from tournament_clean_arch.use_cases.create_tournament_interactor \
            import CreateTournamentInteractor
        use_case = CreateTournamentInteractor(
            storage=storage, presenter=presenter)

        use_case.setup(
            no_of_rounds=tournament_data["no_of_rounds"],
            start_datetime=tournament_data["start_datetime"]
        )

        use_case_response = use_case.execute()

        self.assertEqual(use_case_response, tournament_data)

        self.assertTrue(storage.create_tournament.called)
        args_dict = storage.create_tournament.call_args[1]

        self.assertEqual(
            tournament_data["no_of_rounds"], args_dict.get("no_of_rounds"))
        self.assertEqual(
            tournament_data["start_datetime"], args_dict.get("start_datetime"))

        self.assertTrue(storage.get_tournament.called)
        args_dict = storage.get_tournament.call_args[1]
        self.assertEqual(tournament_id, args_dict["tournament_id"])

        self.assertTrue(presenter.present_create_tournament.called)
        args_dict = presenter.present_create_tournament.call_args[1]

        self.assertEqual(args_dict.get("tournament_details"),
                         tournament_data_with_date_as_obj)

    def test_create_tournament_rounds_gte_3(self):
        tournament_date_time = \
            datetime.datetime.now() + datetime.timedelta(days=1)
        tournament_data = {
            "tournament_id": 1,
            "no_of_rounds": 2,
            "start_datetime":
                tournament_date_time.strftime("%m/%d/%Y, %H:%M:%S")
        }
        tournament_data_with_date_as_obj = copy.deepcopy(tournament_data)
        tournament_data_with_date_as_obj["start_datetime"] = \
            tournament_date_time

        storage = Mock()
        presenter = Mock()

        tournament_id = tournament_data["tournament_id"]
        storage.create_tournament.return_value = tournament_id
        storage.get_tournament.return_value = tournament_data_with_date_as_obj
        presenter.present_create_tournament.return_value = tournament_data

        from tournament_clean_arch.use_cases.create_tournament_interactor \
            import CreateTournamentInteractor
        use_case = CreateTournamentInteractor(
            storage=storage, presenter=presenter)

        use_case.setup(
            no_of_rounds=tournament_data["no_of_rounds"],
            start_datetime=tournament_data["start_datetime"]
        )

        from tournament_clean_arch.constants.custom_exceptions import \
            InvalidNumberOfRounds
        with self.assertRaises(InvalidNumberOfRounds):
            use_case.execute()
