from django.test import TestCase


class TestPlayMatch(TestCase):
    username = "user1"
    user = None
    match = None

    def test_play_match(self):
        self._populate_user()
        self._create_match()
        from tournament.models.match import Match
        Match.play_match(match_id=self.match.id, user_id=self.user.id)

        self.match = self._get_match()
        self.assertEqual(self.match.status, "IN_PROGRESS")

    def test_play_match_when_tournament_not_started(self):
        from datetime import timedelta
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time
        from tournament.models import Tournament
        from tdd_practice.constants.general import TournamentStatus

        self._populate_user()
        self._create_match()

        curr_datetime = get_current_local_date_time()
        Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime + timedelta(days=1),
            status=TournamentStatus.FULL_YET_TO_START.value)

        with self.assertRaisesMessage(
                Exception, "Can not play match until tournament is started"):
            from tournament.models.match import Match
            Match.play_match(match_id=self.match.id, user_id=self.user.id)

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)

    def _create_match(self):
        from tournament.models import Match
        self.match = Match.objects.create(user_id=self.user.id)

    def _get_match(self):
        from tournament.models.match import Match
        return Match.objects.get(id=self.match.id)