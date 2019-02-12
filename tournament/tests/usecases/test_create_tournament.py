from unittest import TestCase


class TestCreateTournament(TestCase):
    import datetime
    NO_OF_ROUNDS = 4
    START_DATETIME = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")

    def test_create_tournament(self):
        tournament_data = {
            'tournament_id': 1,
            'no_of_rounds': self.NO_OF_ROUNDS,
            'start_datetime': self.START_DATETIME
        }

        tournament_id = tournament_data['tournament_id']

        from copy import deepcopy
        tournament_data_without_id = deepcopy(tournament_data)
        tournament_data_without_id.pop('tournament_id')

        from mock import Mock

        storage = Mock()
        storage.create_tournament.return_value = tournament_id
        storage.get_tournament.return_value = tournament_data_without_id

        presenter = Mock()
        presenter.present_create_tournament.return_value = tournament_data

        from tournament.usecases import CreateTournamentInteractor
        usecase = CreateTournamentInteractor(
            storage=storage, presenter=presenter
        )
        usecase.setup(no_of_rounds=self.NO_OF_ROUNDS, start_datetime=self.START_DATETIME)
        usecase_response = usecase.execute()
        self.assertEqual(usecase_response, tournament_data)

        (no_of_rounds, start_datetime), _ = storage.create_tournament.call_args
        self.assertEqual(no_of_rounds, self.NO_OF_ROUNDS)
        self.assertEqual(start_datetime, self.START_DATETIME)

        (get_tournament_tournament_id,), _ = storage.get_tournament.call_args
        self.assertEqual(get_tournament_tournament_id, tournament_id)

        (presenter_input_tournament_data, presenter_tournament_id), _ = presenter.present_create_tournament.call_args
        self.assertEqual(presenter_tournament_id, tournament_id)
        self.assertEqual(presenter_input_tournament_data, tournament_data_without_id)
