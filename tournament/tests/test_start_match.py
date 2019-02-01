from django.test import TestCase

from tournament.constants.general import TournamentStatus
from ib_common.date_time_utils.convert_string_to_local_date_time \
    import convert_string_to_local_date_time


class TestStartMatch(TestCase):

    def setUp(self):
        self.user =

    def test_user_start_match(self):
        from tournament.models import User, Tournament, UserTournament, \
            TournamentMatch, Match

        player = UserTournament()
        round_number = 3

        user_id = 1
        opponent_player_id = 2

        player.start_match(
            player_id=opponent_player_id, round_number=round_number
        )

        matches = Match.objects.all()
        match = Match.objects.filter(
            tournament_id=tournament.id,
            round_number=round_number
        )
        self.assertEqual(.count, 1)
        self.assertEqual(TournamentMatch.objects.all().count(), 2)

        obj_exists = TournamentMatch.objects.filter(
            round_number=round_number
        ).exists()
        self.assertTrue(obj_exists)

    def create_user(self):
        from tournament.models import User

        user_name = "John"
        user = User.objects.create(name=user_name)

        return user

    def create_tournament(self, user_id):
        from tournament.models import Tournament

        total_rounds = 4
        start_datetime = "2019-12-12 13:00:00"
        date_time_format = '%Y-%m-%d %H:%M:%S'
        start_datetime_obj = convert_string_to_local_date_time(
            start_datetime, date_time_format
        )

        tournament = Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime_obj,
            status=TournamentStatus.CAN_JOIN.value
        )

        return tournament

    def create_user_tournament(self, user_id, tournament_id):
        from tournament.models import UserTournament

        obj = UserTournament.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
        )

        return obj
