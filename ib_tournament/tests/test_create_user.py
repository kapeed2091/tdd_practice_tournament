from django.test import TestCase


class TestCreateUser(TestCase):
    user_details = {
        'username': 'user1',
        'name': 'User 1',
        'age': 22,
        'gender': 'MALE'
    }

    def test_create_user(self):
        from ib_tournament.models import Player
        Player.create_player(self.user_details)
        # TODO: Don't user get_player function
        player = Player.get_player(self.user_details['username'])
        player_details = player.get_player_dict()
        self.assertEqual(player_details['username'],
                         self.user_details['username'])

    def test_unique_username(self):
        from ib_tournament.models import Player
        Player.create_player(self.user_details)
        from django_swagger_utils.drf_server.exceptions import BadRequest
        with self.assertRaisesMessage(BadRequest, "Username already Exists"):
            Player.create_player(self.user_details)

    def test_user_fields_updation(self):
        user_details = {
            'username': 'user1',
            'name': 'User 1',
            'age': 22,
            'gender': 'MALE'
        }
        from ib_tournament.models import Player
        Player.create_player(user_details)
        player = Player.objects.get(username=user_details['username'])
        self.assertEqual(player.username, user_details['username'])
        self.assertEqual(player.name, user_details['name'])
        self.assertEqual(player.age, user_details['age'])
        self.assertEqual(player.gender, user_details['gender'])
