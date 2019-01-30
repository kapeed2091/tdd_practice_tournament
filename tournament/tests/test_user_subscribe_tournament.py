from django.test import TestCase


class TestUserSubscribeToTournament(TestCase):
    username = "user1"
    tournament = None
    user = None

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

        from tournament.models.tournament_user import TournamentUser
        TournamentUser.subscribe_user_to_tournament(
            tournament_id=self.tournament.id, username=self.username)
        self._validate_user_subscribed()

    def test_invalid_user_subscribe_to_tournament(self):
        with self.assertRaisesMessage(Exception, "Invalid user"):
            from tournament.models.tournament_user import TournamentUser
            TournamentUser.subscribe_user_to_tournament(
                tournament_id=self.tournament.id, username="user")

    def test_user_already_subscribed(self):
        self._populate_user()
        self._subscribe_user_to_tournament()

        with self.assertRaisesMessage(
                Exception, "User already subscribed to given tournament"):
            from tournament.models.tournament_user import TournamentUser
            TournamentUser.subscribe_user_to_tournament(
                tournament_id=self.tournament.id, username=self.username)

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)

    def _validate_user_subscribed(self):
        from tournament.models.tournament_user import TournamentUser
        TournamentUser.objects.get(user__username=self.username,
                                   tournament_id=self.tournament.id)

    def _subscribe_user_to_tournament(self):
        from tournament.models import TournamentUser
        TournamentUser.objects.create(
            tournament_id=self.tournament.id, user_id=self.user.id)
