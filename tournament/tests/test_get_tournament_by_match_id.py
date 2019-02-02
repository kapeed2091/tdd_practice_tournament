from django.test import TestCase


class TestGetTournamentByMatch(TestCase):
    username = "user1"
    user = None
    match = None
    tournament = None

    def test_get_tournament_by_match_id(self):
        self._populate_user()
        self._create_tournament()
        self._create_match()

        from tournament.models import Match
        tournament = Match.get_tournament_by_match_id(match_id=self.match.id)
        self.assertEqual(self.tournament, tournament)

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)

    def _create_match(self):
        from tournament.models import Match
        self.match = Match.objects.create(user_id=self.user.id,
                                          tournament=self.tournament)

    def _create_tournament(self):
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time
        from datetime import timedelta
        from tournament.models import Tournament

        curr_datetime = get_current_local_date_time()
        from tdd_practice.constants.general import TournamentStatus
        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime + timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value)
