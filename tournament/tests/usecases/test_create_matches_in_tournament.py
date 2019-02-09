import datetime
import mock
from unittest import TestCase


class TestCreateMatchesInTournament(TestCase):
    NO_OF_ROUNDS = 4
    START_DATETIME = datetime.datetime.now()

    def test_create_matches_in_tournament(self):
        storage = mock.Mock()
        presenter = mock.Mock()

        storage.get_tournament_data.return_value = {
            'no_of_rounds': self.NO_OF_ROUNDS,
            'start_datetime': self.START_DATETIME
        }
        presenter.present_create_tournament.return_value = {}

        from tournament.usecases.interactors import \
            CreateMatchesInTournamentInteractor
        create_matches_in_tournament_interactor = \
            CreateMatchesInTournamentInteractor(
                storage=storage, presenter=presenter
            )
        create_matches_in_tournament_interactor.setup(tournament_id=1)
        response = create_matches_in_tournament_interactor.execute()

        (create_matches_data,), _ = storage.create_matches.call_args
        self.assertEqual(2**(self.NO_OF_ROUNDS-1), len(create_matches_data),
                          'Not enough matches')

        self.assertEqual(presenter.present_create_matches_in_tournament.return_value,
                         response)
        self.assertTrue(presenter.present_create_matches_in_tournament.called)
