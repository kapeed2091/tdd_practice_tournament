from django.test import TestCase


class TestPlayMatch(TestCase):
    username = "user1"
    user = None
    match = None

    def test_play_match(self):
        from tdd_practice.constants.general import TournamentStatus

        self._populate_user()
        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)
        self._create_user_match()
        from tournament.models.match import Match
        Match.play_match(match_id=self.match.id, user_id=self.user.id)

        self.match = self._get_match()
        self.assertEqual(self.match.status, "IN_PROGRESS")

    def test_play_match_when_tournament_not_started(self):
        from tdd_practice.constants.general import TournamentStatus

        self._populate_user()
        self._create_tournament(status=TournamentStatus.FULL_YET_TO_START.value)
        self._create_user_match()

        with self.assertRaisesMessage(
                Exception, "User can not play match until match is started"):
            from tournament.models.match import Match
            Match.play_match(match_id=self.match.id, user_id=self.user.id)

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)

    def _create_user_match(self):
        from tournament.models import RoundMatch
        self.match = RoundMatch.objects.create(
            tournament_id=self.tournament.id, round_no=1)

        from tournament.models import Match
        Match.objects.create(
            user_id=self.user.id, tournament=self.tournament,
            round_match_id=self.match.id)

    def _get_match(self):
        from tournament.models.match import Match
        return Match.objects.get(id=self.match.id)

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
