from django.test import TestCase


class TestGetuserCurrentRound(TestCase):
    username = "user1"
    user = None
    tournament = None
    curr_round_no = 2

    def test_get_user_current_round_no(self):
        from tdd_practice.constants.general import TournamentStatus

        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)
        self._populate_user()
        self._create_user_matches()

        from tournament.models import Match
        curr_round_no = Match.get_user_current_round_no(
            tournament_id=self.tournament.id, user_id=self.user.id)

        self.assertEqual(self.curr_round_no, curr_round_no)

    def _create_tournament(self, status):
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time
        from datetime import timedelta
        from tournament.models import Tournament

        curr_datetime = get_current_local_date_time()
        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime + timedelta(days=1),
            status=status)

    def _create_user_matches(self):
        from tournament.models import RoundMatch
        match = RoundMatch.objects.create(
            tournament_id=self.tournament.id, round_no=1)

        from tournament.models import Match
        Match.objects.create(
            user_id=self.user.id, tournament=self.tournament,
            round_match_id=match.id)

        curr_match = RoundMatch.objects.create(
            tournament_id=self.tournament.id, round_no=self.curr_round_no)

        from tournament.models import Match
        Match.objects.create(
            user_id=self.user.id, tournament=self.tournament,
            round_match_id=curr_match.id)

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)
