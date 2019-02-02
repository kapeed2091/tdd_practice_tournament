from django.test import TestCase
from tournaments.constants.general import TournamentStatus


class TestSubscribeToTournament(TestCase):
    tournament = None
    user = None
    user_2 = None

    def test_case_subscribe_to_tournament(self):
        from tournaments.models import UserTournament
        self.create_user()
        self.create_tournament(user_id=self.user.id)

        UserTournament.subscribe_to_tournament(
            user_id=self.user.id, tournament_id=self.tournament.id
        )

        is_user_subscribed = UserTournament.objects.filter(
            user_id=self.user.id, tournament_id=self.tournament.id
        ).exists()

        self.assertEqual(UserTournament.objects.all().count(), 1)
        self.assertTrue(is_user_subscribed)

    def test_case_invalid_tournament_id(self):
        from tournaments.models import UserTournament
        self.create_user()
        tournament_id = 1

        from tournaments.exceptions.custom_exceptions import InvalidTournamentId
        with self.assertRaises(InvalidTournamentId):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=tournament_id
            )

    def test_case_invalid_user_id(self):
        from tournaments.models import UserTournament

        user_id = 1
        self.create_tournament(user_id=user_id)

        from tournaments.exceptions.custom_exceptions import InvalidUserId
        with self.assertRaises(InvalidUserId):
            UserTournament.subscribe_to_tournament(
                user_id=user_id, tournament_id=self.tournament.id
            )

    def test_case_user_already_registered(self):
        from tournaments.models import UserTournament
        self.create_user()
        self.create_tournament(user_id=self.user.id)
        self.create_user_tournament()

        from tournaments.exceptions.custom_exceptions import UserAlreadyRegistered
        with self.assertRaises(UserAlreadyRegistered):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=self.tournament.id
            )

    def test_case_user_registering_tournament_which_is_full(self):
        from tournaments.models import UserTournament
        self.create_user()
        self.create_tournament(
            user_id=self.user.id,
            status=TournamentStatus.FULL_YET_TO_START.value
        )

        from tournaments.exceptions.custom_exceptions import \
            InvalidFullYetToStartRegister
        with self.assertRaises(InvalidFullYetToStartRegister):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=self.tournament.id
            )

    def test_case_user_registering_tournament_which_is_in_progress(self):
        from tournaments.models import UserTournament
        self.create_user()
        self.create_tournament(
            user_id=self.user.id,
            status=TournamentStatus.IN_PROGRESS.value
        )

        from tournaments.exceptions.custom_exceptions import InvalidInProgresstRegister
        with self.assertRaises(InvalidInProgresstRegister):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=self.tournament.id
            )

    def test_case_user_registering_tournament_which_is_completed(self):
        from tournaments.models import UserTournament
        self.create_user()
        self.create_tournament(
            user_id=self.user.id,
            status=TournamentStatus.COMPLETED.value
        )

        from tournaments.exceptions.custom_exceptions import InvalidCompletedRegister
        with self.assertRaises(InvalidCompletedRegister):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=self.tournament.id
            )

    def test_case_user_is_last_person_to_join_tournament(self):
        from tournaments.models import UserTournament, Tournament
        self.create_user()
        self.create_second_user()
        self.create_tournament(user_id=self.user.id)
        self.create_user_tournament()

        UserTournament.subscribe_to_tournament(
            user_id=self.user_2.id, tournament_id=self.tournament.id
        )

        tournament = Tournament.objects.get(id=self.tournament.id)

        self.assertEqual(
            tournament.status, TournamentStatus.FULL_YET_TO_START.value
        )

    def create_tournament(
            self, user_id, status=TournamentStatus.CAN_JOIN.value):
        from tournaments.models import Tournament

        total_rounds = 1
        start_datetime = "2019-12-12 13:00:00"

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        date_time_format = '%Y-%m-%d %H:%M:%S'

        start_datetime = convert_string_to_local_date_time(
            start_datetime, date_time_format
        )
        tournament = Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime,
            status=status
        )
        self.tournament = tournament

    def create_user(self):
        from tournaments.models import User

        user_name = "John"

        user = User.objects.create(name=user_name)
        self.user = user

    def create_second_user(self):
        from tournaments.models import User

        user_name = "John Abraham"

        user = User.objects.create(name=user_name)
        self.user_2 = user

    def create_user_tournament(self):
        from tournaments.models import UserTournament
        from tournaments.constants.general import UserTournamentStatus

        UserTournament.objects.create(
            user_id=self.user.id,
            tournament_id=self.tournament.id,
            status=UserTournamentStatus.ALIVE.value
        )
