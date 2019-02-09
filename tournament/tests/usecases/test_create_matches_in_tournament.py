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

    def test_create_matches_two_players_in_each_match(self):
        storage = mock.Mock()
        presenter = mock.Mock()

        storage.get_tournament_data.return_value = {
            'no_of_rounds': self.NO_OF_ROUNDS,
            'start_datetime': self.START_DATETIME,
            'player_usernames': ['USERNAME_'+str(i+1) for i in range(0, 2**(self.NO_OF_ROUNDS))]
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
        for match in create_matches_data:
            player_usernames = match['player_usernames']
            self.assertEqual(2, len(player_usernames), 'Match should consist of only two players')

        self.assertEqual(presenter.present_create_matches_in_tournament.return_value,
                         response)
        self.assertTrue(presenter.present_create_matches_in_tournament.called)
