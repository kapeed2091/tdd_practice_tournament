from django.test import TestCase

from tdd_practice.constants.general import TournamentStatus


class TestUserSubscribeToTournament(TestCase):
    username = "user1"
    tournament = None
    user = None
    tournament_status = TournamentStatus.CAN_JOIN.value

    def test_user_subscribe_to_tournament(self):
        self._populate_user()
        self._create_tournament()

        from tournament.models.tournament_user import TournamentUser
        TournamentUser.subscribe_user_to_tournament(
            tournament_id=self.tournament.id, username=self.username)
        self._validate_user_subscribed()

    def test_invalid_user_subscribe_to_tournament(self):
        self._create_tournament()
        with self.assertRaisesMessage(Exception, "Invalid user"):
            from tournament.models.tournament_user import TournamentUser
            TournamentUser.subscribe_user_to_tournament(
                tournament_id=self.tournament.id, username="user")

    def test_user_already_subscribed(self):
        self._populate_user()
        self._create_tournament()
        self._subscribe_user_to_tournament()

        with self.assertRaisesMessage(
                Exception, "User already subscribed to given tournament"):
            from tournament.models.tournament_user import TournamentUser
            TournamentUser.subscribe_user_to_tournament(
                tournament_id=self.tournament.id, username=self.username)

    def test_subscribe_to_can_join_status_tournament(self):
        self.tournament_status = TournamentStatus.IN_PROGRESS.value
        self._create_tournament()
        self._populate_user()

        with self.assertRaisesMessage(
                Exception, "User can not join in the tournament"):
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

    def _create_tournament(self):
        from datetime import datetime, timedelta
        from tournament.models import Tournament

        curr_datetime = datetime.now()
        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime + timedelta(days=1),
            status=self.tournament_status)
