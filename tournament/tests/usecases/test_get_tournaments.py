from unittest import TestCase

class TestGetTournaments(TestCase):

    def test_get_tournaments(self):
        import datetime
        tournaments = [
            {
                'tournament_id': 1,
                'no_of_rounds': 4,
                'start_datetime': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")
            }
        ]

        from mock import Mock
        storage = Mock()
        storage.get_tournaments.return_value = tournaments

        presenter = Mock()
        presenter.present_get_tournaments.return_value = tournaments

        from tournament.usecases import GetTournamentsInteractor
        usecase = GetTournamentsInteractor(storage=storage, presenter=presenter)
        usecase_response = usecase.execute()
        self.assertEqual(usecase_response, tournaments)

        self.assertTrue(storage.get_tournaments.called)
        get_tournament_input, _ = storage.get_tournaments.call_args
        self.assertEqual(get_tournament_input, (), 'No arguments for get tournaments storage')

        self.assertTrue(presenter.present_get_tournaments)
        (presenter_get_tournaments_input, ), _ = presenter.present_get_tournaments.call_args
        self.assertEqual(presenter_get_tournaments_input, tournaments)
