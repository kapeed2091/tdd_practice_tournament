import datetime
from django.test import TestCase

from tournament.utils.date_time_utils import get_current_date_time


class TestSubscribeToTournament(TestCase):

    def setUp(self):
        from tournament.models import KoTournament, User

        now = get_current_date_time()
        KoTournament.objects.create(
            created_user_id='User',
            name='Tournament1',
            no_of_rounds=3,
            start_datetime=now + datetime.timedelta(days=1)
        )

        User.objects.create(
            user_id='User2'
        )

    def test_subscribe_to_tournament(self):
        from tournament.models import TournamentUser

        TournamentUser.subscribe_to_tournament(user_id='User2', tournament_id=1)
        tournament_user_objs = TournamentUser.objects.get(user_id='User2', tournament_id=1)
        self.assertEqual(len(tournament_user_objs), 1)

