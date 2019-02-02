from django.test import TestCase

from tournaments.constants.general import TournamentStatus


class TestCreateUserMatch(TestCase):
    def test_create_user_match(self):
        from tournaments.models import UserMatch

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)

        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )
        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        initial_objects_count = UserMatch.objects.all().count()
        UserMatch.create_user_match(user.id, match.id)
        final_objects_count = UserMatch.objects.all().count()

        objects_newly_created_count = \
            final_objects_count - initial_objects_count

        user_match_exists = UserMatch.objects.filter(
            user_id=user.id,
            match_id=match.id
        ).exists()

        self.assertTrue(user_match_exists)
        self.assertEqual(objects_newly_created_count, 1)

    def test_invalid_match_id(self):
        from tournaments.models import UserMatch

        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)
        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )

        match_id = 1

        from tournaments.exceptions.custom_exceptions import InvalidMatchId
        with self.assertRaises(InvalidMatchId):
            UserMatch.create_user_match(user.id, match_id)

    def test_invalid_user_id(self):
        from tournaments.models import UserMatch
        user = self.create_user()
        tournament = self.create_tournament(user_id=user.id)
        self.create_user_tournament(
            user_id=user.id, tournament_id=tournament.id
        )
        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        user_id = 2

        from tournaments.exceptions.custom_exceptions import InvalidUserId
        with self.assertRaises(InvalidUserId):
            UserMatch.create_user_match(user_id, match.id)

    def test_user_not_in_tournament(self):
        from tournaments.models import UserMatch
        user = self.create_user()
        user_2 = self.create_second_user()

        tournament = self.create_tournament(user_id=user.id)

        round_number = 2
        match = self.create_match(
            tournament_id=tournament.id, round_number=round_number
        )

        from tournaments.exceptions.custom_exceptions import \
            UserNotInTournamnet
        with self.assertRaises(UserNotInTournamnet):
            UserMatch.create_user_match(user_2.id, match.id)

    @staticmethod
    def create_tournament(
            user_id, status=TournamentStatus.IN_PROGRESS.value):
        from tournaments.models import Tournament

        total_rounds = 4

        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        start_datetime = get_current_local_date_time()

        tournament = Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime,
            status=status
        )

        return tournament

    @staticmethod
    def create_user():
        from tournaments.models import User

        user_name = "John"

        user = User.objects.create(name=user_name)
        return user

    @staticmethod
    def create_match(tournament_id, round_number):
        from tournaments.models import Match

        match = Match.objects.create(
            tournament_id=tournament_id,
            round_number=round_number
        )

        return match

    @staticmethod
    def create_second_user():
        from tournaments.models import User

        user_name = "John-2"

        user = User.objects.create(name=user_name)
        return user

    @staticmethod
    def create_user_tournament(user_id, tournament_id):
        from tournaments.models import UserTournament

        obj = UserTournament.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
        )
        return obj
