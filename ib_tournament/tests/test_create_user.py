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
        player = Player.objects.get(username=self.user_details['username'])
        self.assertEqual(player.username, self.user_details['username'])

    def test_unique_username(self):
        from ib_tournament.models import Player
        Player.create_player(self.user_details)
        from django_swagger_utils.drf_server.exceptions import BadRequest
        with self.assertRaisesMessage(BadRequest, "Username already Exists"):
            Player.create_player(self.user_details)

    def test_user_fields_updation(self):
        from ib_tournament.models import Player
        Player.create_player(self.user_details)
        player = Player.objects.get(username=self.user_details['username'])
        self.assertEqual(player.username, self.user_details['username'])
        self.assertEqual(player.name, self.user_details['name'])
        self.assertEqual(player.age, self.user_details['age'])
        self.assertEqual(player.gender, self.user_details['gender'])
