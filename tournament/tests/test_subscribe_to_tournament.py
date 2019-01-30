from django.test import TestCase
from tournament.constants.general import TournamentStatus


class TestSubscribeToTournament(TestCase):
    tournament = None
    user = None
    user_2 = None

    def testcase_subscribe_to_tournament(self):
        from tournament.models import UserTournament
        self.create_user()
        self.create_tournament(user_id=self.user.id)

        UserTournament.subscribe_to_tournament(
            user_id=self.user.id, tournament_id=self.tournament.id
        )

        user_tournaments = UserTournament.objects.all()
        user_tournament = user_tournaments[0]

        self.assertEqual(user_tournaments.count(), 1)
        self.assertEqual(user_tournament.user_id, self.user.id)
        self.assertEqual(user_tournament.tournament_id, self.tournament.id)

    def test_case_invalid_tournament_id(self):
        from tournament.models import UserTournament
        self.create_user()
        tournament_id = 1

        from tournament.exceptions.exceptions import InvalidTournamentId
        with self.assertRaises(InvalidTournamentId):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=tournament_id
            )

    def test_case_invalid_user_id(self):
        from tournament.models import UserTournament

        user_id = 1
        self.create_tournament(user_id=user_id)

        from tournament.exceptions.exceptions import InvalidUserId
        with self.assertRaises(InvalidUserId):
            UserTournament.subscribe_to_tournament(
                user_id=user_id, tournament_id=self.tournament.id
            )

    def test_case_user_already_registered(self):
        from tournament.models import UserTournament
        self.create_user()
        self.create_tournament(user_id=self.user.id)
        self.create_user_tournament()

        from tournament.exceptions.exceptions import UserAlreadyRegistered
        with self.assertRaises(UserAlreadyRegistered):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=self.tournament.id
            )

    def test_case_user_registering_tournament_which_is_full(self):
        from tournament.models import UserTournament
        self.create_user()
        self.create_tournament(
            user_id=self.user.id,
            status=TournamentStatus.FULL_YET_TO_START.value
        )

        from tournament.exceptions.exceptions import \
            InvalidFullYetToStartRegister
        with self.assertRaises(InvalidFullYetToStartRegister):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=self.tournament.id
            )

    def test_case_user_registering_tournament_which_is_in_progress(self):
        from tournament.models import UserTournament
        self.create_user()
        self.create_tournament(
            user_id=self.user.id,
            status=TournamentStatus.IN_PROGRESS.value
        )

        from tournament.exceptions.exceptions import InvalidInProgresstRegister
        with self.assertRaises(InvalidInProgresstRegister):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=self.tournament.id
            )

    def test_case_user_registering_tournament_which_is_completed(self):
        from tournament.models import UserTournament
        self.create_user()
        self.create_tournament(
            user_id=self.user.id,
            status=TournamentStatus.COMPLETED.value
        )

        from tournament.exceptions.exceptions import InvalidCompletedRegister
        with self.assertRaises(InvalidCompletedRegister):
            UserTournament.subscribe_to_tournament(
                user_id=self.user.id, tournament_id=self.tournament.id
            )

    def test_case_user_is_last_person_to_join_tournament(self):
        from tournament.models import UserTournament, Tournament
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
        from tournament.models import Tournament

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
        from tournament.models import User

        user_name = "John"

        user = User.objects.create(name=user_name)
        self.user = user

    def create_second_user(self):
        from tournament.models import User

        user_name = "John Abraham"

        user = User.objects.create(name=user_name)
        self.user_2 = user

    def create_user_tournament(self):
        from tournament.models import UserTournament

        UserTournament.objects.create(
            user_id=self.user.id,
            tournament_id=self.tournament.id
        )
