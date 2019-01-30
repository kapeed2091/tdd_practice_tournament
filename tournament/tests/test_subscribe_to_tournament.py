import datetime
from django.test import TestCase
from django_swagger_utils.drf_server.exceptions import Forbidden, BadRequest

from tournament.utils.date_time_utils import get_current_date_time


class TestSubscribeToTournament(TestCase):

    users = [
        {
            'user_id': 'User1'
        },
        {
            'user_id': 'User2'
        },
        {
            'user_id': 'User3'
        },
        {
            'user_id': 'User4'
        },
        {
            'user_id': 'User5'
        }
    ]

    def setUp(self):
        from tournament.models import KoTournament, User, TournamentUser

        now = get_current_date_time()
        KoTournament.objects.create(
            created_user_id='User',
            name='Tournament1',
            no_of_rounds=3,
            start_datetime=now + datetime.timedelta(days=1)
        )

        KoTournament.objects.create(
            created_user_id='User',
            name='Tournament1',
            no_of_rounds=3,
            start_datetime=now - datetime.timedelta(days=1)
        )

        tournament3 = KoTournament.objects.create(
            created_user_id='User',
            name='Tournament3',
            no_of_rounds=2,
            start_datetime=now + datetime.timedelta(days=1)
        )

        users_to_create = [
            {
                'user_id': 'User' + str(each)
            } for each in range(1, 5)
        ]
        for each in users_to_create:
            user = User.objects.create(**each)
            TournamentUser.objects.create(
                user=user,
                tournament=tournament3
            )
        User.objects.create(
            user_id='User5'
        )

    def test_subscribe_to_tournament(self):
        from tournament.models import TournamentUser

        tournament_users_before = list(TournamentUser.objects.all())
        TournamentUser.subscribe_to_tournament(user_id='User2', tournament_id=1)
        tournament_users_after = list(TournamentUser.objects.all())

        newly_added_objs = [each for each in tournament_users_after if each not in tournament_users_before]
        self.assertEqual(len(newly_added_objs), 1)

        newly_added_obj = newly_added_objs[0]
        self.assertEqual(newly_added_obj.user.user_id, 'User2')
        self.assertEqual(newly_added_obj.tournament.id, 1)

    def test_subscribe_to_tournament_which_has_started(self):
        from tournament.models import TournamentUser

        with self.assertRaisesMessage(Forbidden, 'Subscription can only be done before starting of the Tournament'):
            TournamentUser.subscribe_to_tournament(user_id='User2', tournament_id=2)

    def test_subscribe_to_tournament_after_reaching_max_members(self):
        from tournament.models import TournamentUser

        with self.assertRaisesMessage(Forbidden, 'There is no place for new subscriptions'):
            TournamentUser.subscribe_to_tournament(user_id='User5', tournament_id=3)

    def test_subscribe_to_tournament_again(self):
        from tournament.models import TournamentUser

        with self.assertRaisesMessage(BadRequest, 'Already subscribed to this tournament'):
            TournamentUser.subscribe_to_tournament(user_id='User2', tournament_id=3)

    def test_subscribe_to_tournament_with_wrong_user_id(self):
        from tournament.models import TournamentUser

        with self.assertRaisesMessage(BadRequest, 'Invalid user id'):
            TournamentUser.subscribe_to_tournament(user_id='User10', tournament_id=3)
