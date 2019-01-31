from django.test import TestCase


class TestPlayTournamentMatch(TestCase):
    tournament = None
    username = "user1"
    user = None

    def test_user_play_tournament_match(self):
        self._populate_user()
        self._create_tournament()
        self._create_tournament_match()

        from tournament.models import Tournament
        Tournament.play_tournament_match(tournament_id=self.tournament.id,
                                         user_id=self.user.id)

        match = self._get_tournament_match()
        self.assertEquals("STARTED", match.status)

    def _create_tournament(self):
        from tournament.models import Tournament
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time
        from tdd_practice.constants.general import TournamentStatus

        start_datetime = get_current_local_date_time()
        tournament_status = TournamentStatus.CAN_JOIN.value

        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=start_datetime,
            status=tournament_status)

    def _create_tournament_match(self):
        from tournament.models import TournamentMatch
        import uuid

        match_id = uuid.uuid4()
        TournamentMatch.objects.create(
            tournament_id=self.tournament.id, round_no=1, match_id=match_id)

    def _get_tournament_match(self):
        from tournament.models import TournamentMatch
        match = TournamentMatch.objects.get(tournament_id=self.tournament.id,
                                            user_id=self.user.id)
        return match

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)
