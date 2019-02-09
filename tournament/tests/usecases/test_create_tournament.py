import datetime
from unittest import TestCase

import mock


class TestCreateTournament(TestCase):

    NO_OF_ROUNDS = 4
    START_DATETIME = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")

    def test_create_tournament(self):
        storage = mock.Mock()
        presenter = mock.Mock()

        storage.get_tournament.return_value = {"a": 1}
        storage.create_tournament.return_value = 10
        presenter.present_create_tournament.return_value = {"b": 2}

        from tournament.usecases.interactors import CreateTournamentInteractor
        create_tournament_interactor = CreateTournamentInteractor(
            storage=storage, presenter=presenter
        )
        create_tournament_interactor.setup(no_of_rounds=self.NO_OF_ROUNDS,
                                           start_datetime=self.START_DATETIME)
        tournament = create_tournament_interactor.execute()

        (no_of_rounds, start_datetime), _ = storage.create_tournament.call_args
        self.assertEqual(self.NO_OF_ROUNDS, no_of_rounds)
        self.assertEqual(self.START_DATETIME, start_datetime)

        (get_tournament_input,), _ = storage.get_tournament.call_args
        self.assertEqual(10, get_tournament_input)

        (presenter_input,), _ = presenter.present_create_tournament.call_args
        self.assertEqual({"a": 1}, presenter_input)

        self.assertEqual(presenter.present_create_tournament.return_value,
                         tournament)

    def test_create_tournament_no_of_rounds_validation(self):
        storage = mock.Mock()
        presenter = mock.Mock()

        from tournament.usecases.interactors import CreateTournamentInteractor
        create_tournament_interactor = CreateTournamentInteractor(
            storage=storage, presenter=presenter
        )
        create_tournament_interactor.setup(no_of_rounds=2,
                                           start_datetime=self.START_DATETIME)

        with self.assertRaises(Exception):
            create_tournament_interactor.execute()

    def test_create_tournament_start_datetime_validation(self):
        storage = mock.Mock()
        presenter = mock.Mock()

        from tournament.usecases.interactors import CreateTournamentInteractor
        create_tournament_interactor = CreateTournamentInteractor(
            storage=storage, presenter=presenter
        )

        start_datetime = datetime.datetime.now() - datetime.timedelta(days=1)
        start_datetime = start_datetime.strftime("%m/%d/%Y, %H:%M:%S")
        create_tournament_interactor.setup(no_of_rounds=self.NO_OF_ROUNDS,
                                           start_datetime=start_datetime)

        with self.assertRaises(Exception):
            create_tournament_interactor.execute()
