from django.test import TestCase


class TestGetTournamentWinner(TestCase):
    username = "user1"
    tournament = None
    user = None

    def test_get_tournament_winner(self):
        self._populate_user()
        from tdd_practice.constants.general import TournamentStatus
        self._create_tournament(status=TournamentStatus.COMPLETED.value,
                                winner=self.user)

        from tournament.models import Tournament
        winner_profile = Tournament.\
            get_tournament_winner_profile(tournament_id=self.tournament.id)

        exp_winner_profile = self._get_expected_winner_profile()
        self.assertEqual(exp_winner_profile, winner_profile)

    def test_tournament_winner_not_declared(self):
        from tdd_practice.constants.general import TournamentStatus
        self._create_tournament(status=TournamentStatus.COMPLETED.value,
                                winner=None)

        from tournament.models import Tournament
        with self.assertRaisesMessage(Exception,
                                      "Tournament winner not yet declared"):
            Tournament.get_tournament_winner_profile(
                tournament_id=self.tournament.id)

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)

    def _create_tournament(self, status, winner):
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time
        from tournament.models import Tournament

        curr_datetime = get_current_local_date_time()
        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime,
            winner=winner,
            status=status)

    def _get_expected_winner_profile(self):
        exp_winner_profile = {
            "user_id": self.user.id,
            "name": self.user.name,
            "gender": self.user.gender,
            "age": self.user.age
        }
        return exp_winner_profile
