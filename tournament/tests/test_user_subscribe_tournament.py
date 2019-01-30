from django.test import TestCase


class TestUserSubscribeToTournament(TestCase):
    username = "user1"
    tournament = None

    def setUp(self):
        from datetime import datetime, timedelta
        from tournament.models import Tournament
        from tdd_practice.constants.general import TournamentStatus

        curr_datetime = datetime.now()
        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime + timedelta(days=1),
            status=TournamentStatus.CAN_JOIN.value)

    def test_user_subscribe_to_tournament(self):
        self._populate_user()

        TournamentUser.subscribe_user_to_tournamament(
            tournament_id=self.tournament.id, username=self.username)
        self._validate_user_subscribed()

    def _populate_user(self):
        from tournament.models.user import User
        User.objects.create(username=self.username)

    def _validate_user_subscribed(self):
        TournamentUser.objects.get(user__username=self.username,
                                   tourmament_id=self.tournament.id)