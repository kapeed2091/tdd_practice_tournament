from django.test import TestCase


class TestUserSubmitMatchScore(TestCase):
    username = "user1"
    user = None
    match = None
    tournament = None

    def test_user_submit_match_score(self):
        from tdd_practice.constants.general import TournamentStatus
        self._populate_user()
        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)
        self._create_match()

        from tournament.models import Match
        user_match_score = {
            "match_id": self.match.id,
            "user_id": self.user.id,
            "score": 50
        }
        Match.user_submit_match_score(user_match_score=user_match_score)

        match = Match.objects.get(id=self.match.id)
        from tdd_practice.constants.general import UserMatchStatus
        self.assertEqual(match.status, UserMatchStatus.COMPLETED.value)
        self.assertEqual(match.score, user_match_score['score'])

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)

    def _create_match(self):
        from tournament.models import Match
        self.match = Match.objects.create(user_id=self.user.id,
                                          tournament=self.tournament)

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
