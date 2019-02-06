from django.test import TestCase


class TestProgressMatchWinner(TestCase):
    username = "user1"
    user = None
    tournament = None

    def test_progress_match_winner_to_next_round(self):
        from tdd_practice.constants.general import TournamentStatus
        self._populate_user()
        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)
        self._create_round_matches()

        winner_id = self.user.id
        curr_round_no = 1

        from tournament.models import RoundMatch
        winner_details = {
            "tournament_id": self.tournament.id,
            "curr_round_no": curr_round_no,
            "winner_id": winner_id
        }
        RoundMatch.progress_match_winner_to_next_round(
            winner_details=winner_details)

        from tournament.models import Match
        match = Match.objects.get(round_match__round_no=curr_round_no+1)
        self.assertEqual(winner_id, match.user_id)

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)

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

    def _create_round_matches(self):
        from tournament.models import RoundMatch

        next_round_no = 2
        no_of_matches = 2
        for index in range(no_of_matches):
            RoundMatch.objects.create(round_no=next_round_no,
                                      tournament_id=self.tournament.id)
