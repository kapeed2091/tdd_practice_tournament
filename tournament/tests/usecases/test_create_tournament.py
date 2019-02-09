from unittest import TestCase

from mock import patch

from tournament.usecases.base_presenter import BasePresenter
from tournament.usecases.base_storage import BaseStorage


class MockStorage(BaseStorage):

    def get_tournament(self, tournament_id):
        pass

    def create_tournament(self, no_of_rounds, start_datetime):
        return 1


class MockPresenter(BasePresenter):

    def present_create_tournament(self, output_data):
        return {

        }


class TestCreateTournament(TestCase):
    import datetime
    NO_OF_ROUNDS = 4
    START_DATETIME = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    @patch("tournament.tests.usecases.test_create_tournament.MockStorage.create_tournament")
    @patch("tournament.tests.usecases.test_create_tournament.MockStorage.get_tournament")
    @patch(
        "tournament.tests.usecases.test_create_tournament.MockPresenter.present_create_tournament")
    def test_create_tournament(self, mocked_presenter, mocked_storage_get_tournamnet, mocked_storage_create_tournamnet):
        from tournament.usecases.interactors import CreateTournamentInteractor
        create_tournament_interactor = CreateTournamentInteractor(
            storage=MockStorage(), presenter=MockPresenter()
        )
        create_tournament_interactor.setup(no_of_rounds=self.NO_OF_ROUNDS,
                                        start_datetime=self.START_DATETIME)
        mocked_presenter.mocked_storage_get_tournamnet.return_value = 10
        tournament = create_tournament_interactor.execute()


        self.assertEqual(mocked_storage_create_tournamnet.called, True)
        (no_of_rounds, start_datetime), _ = mocked_storage_create_tournamnet.call_args
        self.assertEqual(self.NO_OF_ROUNDS, no_of_rounds)
        self.assertEqual(self.START_DATETIME, start_datetime)

        self.assertEqual(mocked_storage_get_tournamnet.called, True)


        # import ipdb; ipdb.set_trace()
        (presenter_input, ), _ = mocked_presenter.call_args
        self.assertEqual(10, presenter_input)

        self.assertEqual(mocked_presenter.called, True)
        self.assertEqual(mocked_presenter.return_value, tournament)
