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

    def test_subscribe_to_valid_tournament(self):
        self._populate_user()
        with self.assertRaisesMessage(
                Exception, "Invalid tournament id"):
            from tournament.models.tournament_user import TournamentUser
            TournamentUser.subscribe_user_to_tournament(
                tournament_id=100, username=self.username)

    def test_change_tournament_status_to_full_yet_start(self):
        self._create_tournament()
        users = self._populate_users()
        self._subscribe_users_to_tournament(users[1:])

        from tournament.models.tournament_user import TournamentUser
        TournamentUser.subscribe_user_to_tournament(
            tournament_id=self.tournament.id, username=users[0].username)

        from tournament.models import Tournament
        tournament = Tournament.objects.get(id=self.tournament.id)

        self.assertEquals(TournamentStatus.FULL_YET_TO_START.value,
                          tournament.status)

    def _populate_users(self):
        from tournament.models.user import User
        no_of_rounds = self.tournament.no_of_rounds
        no_of_participants = 2**no_of_rounds

        users = []
        for index in range(no_of_participants):
            users.append(User.objects.create(username="user"+str(index+1)))
        return users

    def _subscribe_users_to_tournament(self, users):
        from tournament.models import TournamentUser

        for user in users:
            TournamentUser.objects.create(
                tournament_id=self.tournament.id, user_id=user.id)

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
